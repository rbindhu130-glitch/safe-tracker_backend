from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    class Config:
        orm_mode = True

class VolunteerBase(BaseModel):
    fullname: str
    age: int
    gender: str
    mobile: str
    email: EmailStr
    address: str
    availability: Optional[str] = None

class VolunteerCreate(VolunteerBase):
    id_proof_path: Optional[str] = None

class VolunteerResponse(VolunteerBase):
    id: int
    id_proof_path: Optional[str] = None
    created_at: datetime
    class Config:
        orm_mode = True


class IncidentBase(BaseModel):
    location: str
    category: str
    description: str
    contact: Optional[str] = None
    status: Optional[str] = None


class IncidentCreate(IncidentBase):
    pass        


class IncidentStatusUpdate(BaseModel):
    status: str


class IncidentResponse(IncidentBase):
    id: int
    owner_id: int
    owner: UserResponse
    status: str
    photo_path: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True


class IncidentCreateResponse(BaseModel):
    id: int
    owner_id: int
    owner: UserResponse
    photo_path: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True

