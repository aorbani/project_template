from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
class Base(DeclarativeBase):
    pass

class Message(Base):
    __tablename__ = "Message"
    __table_args__ = {"schema" : "AURAS",'implicit_returning':False}
    msg_id:  Mapped[int] = mapped_column(primary_key=True)
    thread_id:  Mapped[int]
    msg_content:  Mapped[str] =  mapped_column(String(5000))
    sender:  Mapped[str] =  mapped_column(String(20))
    action:   Mapped[str] =  mapped_column(String(5000))
    params:   Mapped[str] =  mapped_column(String(5000))
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class Thread(Base):
    __tablename__ = "Thread"
    __table_args__ = {"schema" : "AURAS"}
    thread_id:  Mapped[int] = mapped_column(primary_key=True)
    user_id:  Mapped[str]=  mapped_column(String(50))
    device_id:  Mapped[str] =  mapped_column(String(100))
    channel:  Mapped[str] =  mapped_column(String(20))
    active:   Mapped[bool]
    params:   Mapped[str] =  mapped_column(String(5000))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_activity: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    expired_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))