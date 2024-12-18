from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
class Base(DeclarativeBase):
    pass

class ComplaintClassification(Base):
    __tablename__ = "ComplaintClassification"
    __table_args__ = {"schema" : "Complaints"}
    id:  Mapped[int] = mapped_column(primary_key=True)
    content:   Mapped[str] =  mapped_column(String(4000))
    channel:Mapped[str] =  mapped_column(String(20))
    class_name:  Mapped[str] =  mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class Classes(Base):
    __tablename__ = "Classes"
    __table_args__ = {"schema" : "Complaints"}
    id:  Mapped[int] = mapped_column(primary_key=True)
    class_key:Mapped[str] =  mapped_column(String(20))
    class_name:  Mapped[str] =  mapped_column(String(20))