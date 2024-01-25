from .routes import *
from approver_backend.api.core import app

app.include_router(files_router)