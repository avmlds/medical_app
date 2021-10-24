from pydantic import BaseModel


class NewDiagnostic(BaseModel):
    name: str
    expired_in_months: int
