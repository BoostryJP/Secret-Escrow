from pydantic import BaseModel


class EOA(BaseModel):
    address: str
    private_key: bytes | None
