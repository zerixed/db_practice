from database import Base
from sqlalchemy import BigInteger, Column, Integer, String
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    username = Column(String,nullable=True)
    name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    about = Column(String, nullable=True)