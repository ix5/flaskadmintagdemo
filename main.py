from app import app, db

from admin import admin
from models import *

if __name__ == '__main__':
    db.create_all()
    app.debug = True
    app.run()
