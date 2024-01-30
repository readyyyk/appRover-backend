from fastapi import APIRouter
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from os import getenv
from datetime import timedelta


pass_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login/form')
SECRET_KEY = getenv('SECRET_KEY')
ALGORITHM = 'HS256'

ACCESS_EXPIRE_DELTA = timedelta(minutes=float(getenv('ACCESS_MINUTES_EXPIRE')))
REFRESH_EXPIRE_DELTA = timedelta(days=float(getenv('REFRESH_DAYS_EXPIRE')))

app = APIRouter()


@app.get('/')
async def index():
    return {
        'docs': '/docs'
    }
