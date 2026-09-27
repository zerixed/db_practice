from database import Base
from sqlalchemy import BigInteger, Column, Integer, String
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=True)
    username = Column(String,nullable=True)
    first_name = Column(String,nullable=True)