from pydantic import BaseModel

class StudentInput(BaseModel):
    school: str
    sex: str
    age: int
    address: str
    famsize: str
    Pstatus: str
    Medu: int
    Fedu: int
    internet: str
    studytime: int
    failures: int
    absences: int
    subject: str