from pydantic import BaseModel


class NewDoctor(BaseModel):
    name: str
    expires_in_days: int
