from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)  # government / academic / traditional
    description = Column(Text, nullable=True)


class OfflineForm(Base):
    __tablename__ = "offline_forms"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    title = Column(String, nullable=False)
    template_path = Column(String, nullable=False)  # path to the PDF template file


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    form_id = Column(Integer, ForeignKey("offline_forms.id"), nullable=False)
    reference_code = Column(String, nullable=True)
    mailed_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, nullable=False, default="drafted")  # drafted / mailed / received / result
    created_at = Column(DateTime(timezone=True), server_default=func.now())