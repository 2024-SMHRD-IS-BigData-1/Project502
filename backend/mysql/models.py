from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from mysql.database import Base
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = 'users'

    id = Column(String(50), primary_key=True, index=True)
    pw = Column(String(1500), nullable=False)
    nick = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), index=True)
    gender = Column(String(10))
    phoneNumber = Column(String(20), nullable=False)
    profile_image_url = Column(String(1000), default="swit.png")
    profile_introduce = Column(String(1500), default="반갑습니다", nullable=True)
    # verification_code = Column(String(50), nullable=True)
    # code_expiration = Column(DateTime, nullable=True)

class Post(Base):
    __tablename__ = 'posts'

    post_idx = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String(50), ForeignKey("users.id"))
    nick = Column(String(20), ForeignKey("users.nick"), nullable=False)
    title = Column(String(1200), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(30), nullable=False)
    posted_at = Column(DateTime(timezone=True), server_default=func.now())
    likes = Column(Integer)
    views = Column(Integer)

    images = relationship("Image", back_populates="post")

class Image(Base):
    __tablename__ = 'images'

    img_idx = Column(Integer, primary_key=True, autoincrement=True)
    post_idx = Column(Integer, ForeignKey("posts.post_idx"))
    img_name = Column(String(1000))
    img_rnmae = Column(String(50))
    size = Column(Integer)
    ext = Column(String(10))

    post = relationship("Post", back_populates="images")
    
class Room(Base):
    __tablename__ = 'rooms'

    room_idx = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id = Column(String(50), ForeignKey('users.id'), index=True)
    opened_at = Column(DateTime)
    partner_id = Column(String(50))

class Chat(Base):
    __tablename__ = 'chats'

    chat_idx = Column(Integer, primary_key=True, autoincrement=True, index=True)
    room_idx = Column(Integer, ForeignKey("rooms.room_idx"), index=True)
    chatter = Column(String(50))
    chat = Column(Text)
    chatted_at = Column(DateTime(timezone=True))
    