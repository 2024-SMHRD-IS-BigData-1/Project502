from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
from datetime import datetime
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

class ChatBase(BaseModel):
    room_idx : int
    chatter : str
    chat: str

class RoomBase(BaseModel):
    id : str
    partner_id : str

class ImageBase(BaseModel):
    post_idx: int
    img_name: str
    img_rnmae: str

class PostBase(BaseModel):
    id : str
    nick : str
    title : str
    content : str
    category : str

class UserBase(BaseModel):
    id : str
    pw : str
    nick : str

class UserCreate(UserBase):
    pw : str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/chats/", status_code=status.HTTP_201_CREATED)
async def create_chat(chat: ChatBase, db: db_dependency):
    db_chat = models.Chat(**chat.dict(), chatted_at=datetime.utcnow())
    db.add(db_chat)
    db.commit()

    return {"message": "Chat message created successfully"}

@app.post("/rooms/", status_code=status.HTTP_201_CREATED)
async def create_room(room: RoomBase, db: db_dependency):
    db_room = models.Room(**room.dict(), opened_at=datetime.utcnow())
    db.add(db_room)
    db.commit()

@app.post("/images/", status_code=status.HTTP_201_CREATED)
async def create_image(image: ImageBase, db: db_dependency):
    db_image = models.Image(**image.dict())
    db.add(db_image)
    db.commit()

@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase, db: db_dependency):
    db_post = models.Post(**post.dict(), posted_at=datetime.utcnow())
    db.add(db_post)
    db.commit()

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    hashed_password = get_password_hash(user.pw)
    db_user = models.User(id=user.id, pw=hashed_password, nick=user.nick)
    db.add(db_user)
    db.commit()

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: str, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user
