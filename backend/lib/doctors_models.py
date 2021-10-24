from pydantic import BaseModel


class NewDoctor(BaseModel):
    name: str
    expired_in_months: int
