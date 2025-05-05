from pydantic import BaseModel, Field

class ToDosSchema(BaseModel):
    title:str = Field(min_length=3)
    description:str = Field(min_length=3,max_length=100)
    priority:int = Field(gt=0,lt=6)
    complete:bool