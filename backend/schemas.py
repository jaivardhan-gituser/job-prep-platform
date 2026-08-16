from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None


class UserOut(BaseModel):
    id: int
    email: str
    full_name: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

from datetime import datetime as dt


class OrganizationOut(BaseModel):
    id: int
    name: str
    category: str
    description: str | None

    class Config:
        from_attributes = True


class OfflineFormOut(BaseModel):
    id: int
    organization_id: int
    title: str
    template_path: str

    class Config:
        from_attributes = True


class SubmissionCreate(BaseModel):
    form_id: int


class SubmissionUpdate(BaseModel):
    reference_code: str | None = None
    mailed_date: dt | None = None
    status: str | None = None


class SubmissionOut(BaseModel):
    id: int
    user_id: int
    form_id: int
    reference_code: str | None
    mailed_date: dt | None
    status: str
    created_at: dt

    class Config:
        from_attributes = True