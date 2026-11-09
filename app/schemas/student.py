from pydantic import BaseModel, ConfigDict, EmailStr, Field

class StudentCreate(BaseModel):
    name: str = Field(min_length=2,max_length=100)
    email: EmailStr
    age: int = Field(ge=16,le=100,strict=True)
    department: str = Field(min_length=2,max_length=100)

class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    age: int
    department: str

class StudentUpdate(BaseModel):
    name:str = Field(min_length=2, max_length=100)
    email: EmailStr
    age: int = Field(ge=16,le=100,strict = True)
    department : str = Field(min_length=2,max_length=100)


class StudentPatch(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    email: EmailStr | None = None
    age: int | None = Field(
        default=None,
        ge=16,
        le=100,
        strict=True,
    )
    department: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )



