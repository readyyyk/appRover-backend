from fastapi import APIRouter
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from os import getenv


pass_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')
SECRET_KEY = getenv('SECRET_KEY')
ALGORITHM = 'HS256'

app = APIRouter()
