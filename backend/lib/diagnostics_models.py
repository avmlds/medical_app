from pydantic import BaseModel


class NewDiagnostic(BaseModel):
    name: str
    expires_in_months: int
