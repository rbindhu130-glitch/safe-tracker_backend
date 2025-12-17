from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# --- User Schemas ---
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True

# --- Volunteer Schemas ---
class VolunteerBase(BaseModel):
    fullname: str
    age: int
    gender: str
    mobile: str
    email: EmailStr
    address: str
    availability: Optional[str] = None

class VolunteerCreate(VolunteerBase):
    pass # id_proof will be handled separately via UploadFile

class VolunteerResponse(VolunteerBase):
    id: int
    id_proof_path: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True

# --- Incident Schemas ---
class IncidentBase(BaseModel):
    location: str
    category: str
    description: str
    contact: Optional[str] = None

class IncidentCreate(IncidentBase):
    pass # photo will be handled separately via UploadFile

class IncidentResponse(IncidentBase):
    id: int
    photo_path: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True
