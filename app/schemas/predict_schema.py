from pydantic import BaseModel

class PredictResponse(BaseModel):
    name: str
    desc: str
    pH_value: int