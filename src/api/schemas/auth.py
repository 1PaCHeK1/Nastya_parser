from api.schemas.base import BaseSchema


class SignInSchema(BaseSchema):
    username: str
    password: str


class ResponseAuthSchema(BaseSchema):
    token: str