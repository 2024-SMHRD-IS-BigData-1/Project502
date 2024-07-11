from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dataclasses import dataclass
from typing import Dict
import uuid
import json
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from mysql import models
from mysql.database import engine, SessionLocal, Base

# 데이터베이스 초기화
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Chatting 폴더의 설정
app.mount("/static", StaticFiles(directory="Chatting/static"), name="static")
templates = Jinja2Templates(directory="Chatting/templates")

@dataclass
class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        id = str(uuid.uuid4())
        self.active_connections[id] = websocket
        await self.send_message(websocket, json.dumps({"isMe": True, "data": "채팅방이 생성되었습니다.", "username": "You"}))

    async def send_message(self, ws: WebSocket, message: str):
        await ws.send_text(message)

    def find_connection_id(self, websocket: WebSocket):
        websocket_list = list(self.active_connections.values())
        id_list = list(self.active_connections.keys())
        pos = websocket_list.index(websocket)
        return id_list[pos]

    async def broadcast(self, webSocket: WebSocket, data: str):
        decoded_data = json.loads(data)
        for connection in self.active_connections.values():
            is_me = False
            if connection == webSocket:
                is_me = True
            await connection.send_text(json.dumps({"isMe": is_me, "data": decoded_data['message'], "username": decoded_data['username']}))

    def disconnect(self, websocket: WebSocket):
        id = self.find_connection_id(websocket)
        del self.active_connections[id]
        return id

connection_manager = ConnectionManager()

@app.get("/", response_class=HTMLResponse)
def get_room(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/message")
async def websocket_endpoint(websocket: WebSocket):
    await connection_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"message received : {data} from : {websocket.client}")
            await connection_manager.broadcast(websocket, data)
    except WebSocketDisconnect:
        id = connection_manager.disconnect(websocket)
        return RedirectResponse("/")

@app.get("/join", response_class=HTMLResponse)
def get_room(request: Request):
    return templates.TemplateResponse("room.html", {"request": request})

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
    img_rnmae: str

class PostBase(BaseModel):
    id: str
    nick: str
    title: str
    content: str
    category: str

class UserBase(BaseModel):
    id: str
    pw: str
    nick: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/chats/", status_code=status.HTTP_201_CREATED)
async def create_chat(chat: ChatBase, db: Session = Depends(get_db)):
    db_chat = models.Chat(**chat.dict(), chatted_at=datetime.utcnow())
    db.add(db_chat)
    db.commit()

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

@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase, db: Session = Depends(get_db)):
    db_post = models.Post(**post.dict(), posted_at=datetime.utcnow())
    db.add(db_post)
    db.commit()

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: Session = Depends(get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user

# 메인 엔트리 포인트
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
