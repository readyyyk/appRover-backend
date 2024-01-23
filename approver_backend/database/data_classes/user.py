from .core import *


class UserLogin(BaseModel):
    username: str
    password: str


class UserInfo(BaseModel):
    id: int
    username: str
    image: str

# from approver_backend.database import UserModel
# user = UserInfo.model_validate(UserModel(...))
