from pydantic import BaseModel
from typing import List

class ContactInfo(BaseModel):
    emails: List[str]
    phone_numbers: List[str]

class BrandData(BaseModel):
    title: str
    description: str
    logo: str
    contact_details: ContactInfo
