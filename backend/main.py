from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect, Depends, HTTPException, status, Form, File, UploadFile, Body
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional, Dict
import uuid
import json
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from mysql import models
from mysql.database import engine, SessionLocal
from passlib.context import CryptContext
import shutil
import os
import bcrypt
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException
from mysql.models import Image
import random


import ai2, weatherAPI, new_location
# 환경 변수에서 API Key와 Secret Key를 불러옵니다.
api_key = os.getenv("COOLSMS_API_KEY")
api_secret = os.getenv("COOLSMS_API_SECRET")

if not isinstance(api_key, str) or not isinstance(api_secret, str):
    raise ValueError("API Key and Secret Key must be set as environment variables and must be strings")


# 데이터베이스 초기화
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

DEFAULT_PROFILE_IMAGE_URL = "/img/swit.png"

# CORS 설정
origins = [
    "http://localhost",
    "http://localhost:3000",  # React 애플리케이션의 주소
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Chatting 폴더의 설정
app.mount("/static", StaticFiles(directory="Chatting/static"), name="static")
templates = Jinja2Templates(directory="Chatting/templates")

# 웹소켓 관련 코드
@dataclass
class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: Dict[str, WebSocket] = {}  # 사용자 ID를 키로 사용

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        await self.send_message(user_id, "채팅방에 연결되었습니다.")

    async def send_message(self, user_id: str, message: str):
        websocket = self.active_connections.get(user_id)
        if websocket:
            await websocket.send_text(message)

    # def find_connection_id(self, websocket: WebSocket):
    #     websocket_list = list(self.active_connections.values())
    #     id_list = list(self.active_connections.keys())
    #     pos = websocket_list.index(websocket)
    #     return id_list[pos]

    async def broadcast(self, from_user_id: str, message: str):
        for user_id, websocket in self.active_connections.items():
            is_me = user_id == from_user_id
            await websocket.send_text(json.dumps({"isMe": is_me, "message": message, "username": from_user_id}))

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

connection_manager = ConnectionManager()

@app.get("/", response_class=HTMLResponse)
def get_room(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/message")
async def websocket_endpoint(websocket: WebSocket, token: str):
    user_id = get_current_user(token)
    await connection_manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Message received: {data} from user: {user_id}")
            await connection_manager.broadcast(user_id, data)
    except WebSocketDisconnect:
        connection_manager.disconnect(user_id)

@app.get("/join", response_class=HTMLResponse)
def get_room_join(request: Request):
    return templates.TemplateResponse("room.html", {"request": request})

# 비밀번호 해싱
pwd_context = CryptContext(schemes=["argon2", "sha256_crypt"], deprecated="auto")

# 비밀번호 해싱
def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

# 비밀번호 검증
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# MySQL 폴더의 설정


class ChatBase(BaseModel):
    room_idx: int
    chatter: str
    chat: str

class RoomBase(BaseModel):
    id: str
    partner_id: str

class ImageBase(BaseModel):
    post_idx: int
    img_name: str

class PostBase(BaseModel):
    id: str
    nick: str
    title: str
    content: str
    category: str
    image_urls: List[str]  # 이미지 URL 리스트

class UserUpdate(BaseModel):
    nick: str # 닉네임은 변경하지 않음
    profile_image_url: Optional[str] = None
    profile_introduce: Optional[str] = None

class SMSRequest(BaseModel):
    phoneNumber: str

class Login(BaseModel):
    username: str
    password: str

class UserBase(BaseModel):
    id: str
    pw: str
    nick: str
    email: str
    gender: str
    phoneNumber: str
    profile_image_url: str
    profile_introduce: Optional[str] = None

class UserCreate(UserBase):
    id: str
    pw: str
    nick: str
    email: str
    gender: str
    phoneNumber: str

# JWT 비밀 키와 알고리즘 설정
SECRET_KEY = "your-secret-key"  # 이 키는 안전하게 보관하고, 실제 배포 시에는 환경 변수로 설정하세요.
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 토큰 만료 시간 설정 (30분)

# 토큰 생성 함수
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 토큰 검증 함수
def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
    
# 현재 사용자 정보 가져오기
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    return user_id


def generate_verification_code() -> str:
    return str(random.randint(100000, 999999))

# SMS 전송 함수
async def send_sms(phoneNumber: str, message: str):
    params = dict()
    params['type'] = 'sms' # Message type ( sms, lms, mms, ata )
    params['to'] = phoneNumber # Recipients Number '01000000000,01000000001'
    params['from'] = '01065078908' # Sender number
    params['text'] = message # Message

    cool = Message(api_key, api_secret)
    try:
        response = cool.send(params)
        print("Success Count : %s" % response['success_count'])
        print("Error Count : %s" % response['error_count'])
        print("Group ID : %s" % response['group_id'])

        if "error_list" in response:
            print("Error List : %s" % response['error_list'])

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)

# 사용자 인증을 위한 함수
def authenticate_user(id: str, password: str, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()  # id 필드로 검색
    if not user:
        return False
    if not verify_password(password, user.pw):
        return False
    return user

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/send-sms/", response_model=dict)
async def send_verification_sms(sms_request: SMSRequest, db: Session = Depends(get_db)):
    phoneNumber = sms_request.phoneNumber
    code = generate_verification_code()  # 인증 코드를 생성합니다.
    message = f"[Swit.]의 인증번호는 {code}입니다."
    
    # SMS 발송 로직 호출
    await send_sms(phoneNumber, message)
    
    # 인증 코드를 데이터베이스에 저장하지 않고 응답으로만 반환
    return {"detail": "SMS sent successfully", "code": code}

@app.post("/chats/", status_code=status.HTTP_201_CREATED)
async def create_chat(chat: ChatBase, db: Session = Depends(get_db)):
    room = db.query(models.Room).filter(models.Room.room_idx == chat.room_idx).first()
    if not room:
        raise HTTPException(status_code=400, detail="Invalid room_idx")
    
    db_chat = models.Chat(**chat.dict(), chatted_at=datetime.utcnow())
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return {"message": "Chat saved successfully", "chat": db_chat}

@app.post('/chat')
def chat_endpoint():
    return {'message': 'Chat request received'}

@app.post("/rooms/", status_code=status.HTTP_201_CREATED)
async def create_room(room: RoomBase, db: Session = Depends(get_db)):
    db_room = models.Room(**room.dict(), opened_at=datetime.utcnow())
    db.add(db_room)
    db.commit()

@app.post("/images/", status_code=status.HTTP_201_CREATED)
async def create_image(image: ImageBase, db: Session = Depends(get_db)):
    db_image = models.Image(**image.dict())
    db.add(db_image)
    db.commit()

@app.get("/posts/", status_code=status.HTTP_201_CREATED)
async def show_image_list(db: Session = Depends(get_db)):
    db_images = db.query(Image).all()
    result = []
    pre_post_idx = 0

    # for image in db_images:
    #     post_idx = image.post_idx
    #     if post_idx != pre_post_idx:
    #         result.append({"post_idx": post_idx, "img_name" : []})
    #         result[-1]["img_name"].append(image.img_name)
    #     else:
    #         result[-1]["img_name"].append(image.img_name)
    #     pre_post_idx = post_idx

    # 포스트와 사용자 정보를 함께 가져오기 위한 쿼리
    for image in db_images:
        post_idx = image.post_idx
        post = db.query(models.Post).filter(models.Post.post_idx == post_idx).first()
        user = db.query(models.User).filter(models.User.id == post.id).first() if post else None

        if post:
            if post_idx != pre_post_idx:
                result.append({
                    "post_idx": post_idx,
                    "post_id": post.id,
                    "img_name": [],
                    "content": post.content,
                    "nick": user.nick if user else "Unknown",
                    "profile_image_url": user.profile_image_url if user else "/img/swit.png"
                })
            result[-1]["img_name"].append(image.img_name)
            pre_post_idx = post_idx

    return (result)

@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase, db: Session = Depends(get_db)):
    db_post = models.Post(
        id=post.id,
        nick=post.nick,
        title=post.title,
        content=post.content,
        category=post.category,
        posted_at=datetime.utcnow()
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    # 이미지 URL 저장
    for image_url in post.image_urls:
        db_image = models.Image(
            post_idx=db_post.post_idx,
            img_name=image_url.split("/")[-1],  # 파일 이름만 추출
        )
        db.add(db_image)
        db.commit()

    return {"message": "Post created successfully"}

@app.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    # 여기서 토큰 무효화 로직을 추가할 수 있습니다. (예: 블랙리스트에 추가)
    # 현재는 단순히 성공 메시지를 반환합니다.
    return {"message": "Logged out successfully"}

# 사용자 정보 수정
@app.put("/users/{user_id}", response_model=UserBase)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user)
):
    # 본인 확인 (권한 검증)
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 필드 업데이트: 프로필 사진과 자기소개만 업데이트
    if user_update.profile_image_url is not None:
        print(f"Updating profile image URL: {user_update.profile_image_url}")  # 디버깅
        user.profile_image_url = user_update.profile_image_url
    if user_update.profile_introduce is not None:
        user.profile_introduce = user_update.profile_introduce
    
    db.commit() # 변경사항 커밋
    db.refresh(user) # 변경사항 새로고침

    return user

# 선택한 닉네임을 가진 사용자의 정보를 가져오기 위한 API
@app.get("/users/profile/{nick}", response_model=UserBase)
async def get_user_profile(nick: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.nick == nick).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# FastAPI 서버 코드에서 확인
@app.get("/user-data")
async def get_user_data():
    # 사용자 데이터를 반환하는 코드
    return {"user": "data"}

# 사용자 정보 엔드포인트
@app.get("/users/me", response_model=UserBase)
async def read_me(user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return {"user_id": user_id}

@app.post("/login")
async def login(login_request: Login, db: Session = Depends(get_db)):
    id = login_request.username
    password = login_request.password
    user = authenticate_user(id, password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # 인증 성공 시 JWT 생성 및 반환
    access_token = create_access_token(data={"sub": user.id})
    return JSONResponse(content={"access_token": access_token, "token_type": "bearer"}, status_code=200)

# 인증 실패 시 처리하는 코드
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        content={"error_message": exc.detail},
        status_code=exc.status_code
    )

# @app.post("/users/", response_model=UserBase, status_code=status.HTTP_201_CREATED)
# async def create_user(user: UserBase, db: Session = Depends(get_db)):
#     hashed_password = get_password_hash(user.pw)
#     db_user = models.User(id=user.id, pw=hashed_password, nick=user.nick, email=user.email, gender=user.gender, phoneNumber=user.phoneNumber )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

@app.post("/users/", response_model=UserBase, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.pw)
    db_user = models.User(
        id=user.id,
        pw=hashed_password,
        nick=user.nick,
        email=user.email,
        gender=user.gender,
        phoneNumber=user.phoneNumber
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# 파일 업로드 및 다운로드 관련 설정
target_dir = './test/'
os.makedirs(target_dir, exist_ok=True)

# 프로필 이미지 업로드
@app.post("/profile-upload-images/")
async def profile_upload_images(files: List[UploadFile] = File(...), db: Session = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    file_names = []
    for file in files:
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(target_dir, unique_filename)
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 파일 이름만 포함
        file_names.append(unique_filename)

    # 업로드된 파일의 URL을 사용자 데이터베이스에 업데이트
    if file_names:
        image_url = f"{file_names[0]}"  # 첫 번째 파일의 URL을 사용할 경우
        user = db.query(models.User).filter(models.User.id == current_user_id).first()
        if user:
            user.profile_image_url = image_url
            db.commit()
            db.refresh(user)
    
    return {"file_names": file_names, "image_url": image_url}

# 게시글 이미지 업로드 
@app.post("/upload-images/")
async def upload_images(files: List[UploadFile] = File(...)):
    image_urls = []
    for file in files:
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(target_dir, unique_filename)
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 이미지 URL 생성
        image_url = f"/static/uploads/{unique_filename}"
        image_urls.append(image_url)

    return {"image_urls": image_urls}

@app.post("/uploadFiles", status_code=status.HTTP_201_CREATED)
async def upload_files(files: List[UploadFile], db: Session = Depends(get_db)):
    uploaded_files = []
    for file in files:
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        filename = os.path.join(target_dir, unique_filename)
        with open(filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # DB에 이미지 정보 저장
        db_image = models.Image(
            post_idx=None,  # 실제 post_idx 값을 설정하세요.
            img_name=unique_filename,
            img_rnmae=file.filename  # 실제 파일 이름 저장
        )
        db.add(db_image)
        db.commit()
        
        uploaded_files.append(unique_filename)
    
    return {"filenames": uploaded_files}

# 파일 다운로드 엔드포인트
@app.get("/testfile/{filename}")
async def get_file(filename: str):
    file_path = os.path.join(target_dir, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)

@app.get("/code")
async def root():
    return ai2.data_dict



# 메인 엔트리 포인트
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)