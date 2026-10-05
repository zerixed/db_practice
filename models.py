from database import Base
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    telegram_id: Mapped[int] = mapped_column(
        BigInteger, unique=True, index=True, nullable=False
    )
    username: Mapped[str | None] = mapped_column(default=None)
    name: Mapped[str | None] = mapped_column(default=None)
    age: Mapped[int | None] = mapped_column(default=None)
    gender: Mapped[str | None] = mapped_column(default=None)
    about: Mapped[str | None] = mapped_column(default=None)
    photo_id: Mapped[str | None] = mapped_column(default=None)
class Reaction(Base):
    __tablename__ = "reactions"
    id: Mapped[int] = mapped_column(primary_key=True)
    from_user_id:Mapped[int] = mapped_column(BigInteger,nullable=False)
    to_user_id:Mapped[int] = mapped_column(BigInteger,nullable=False)
    is_like:Mapped[bool] = mapped_column(nullable=False)