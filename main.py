from app import app, db

from admin import admin

if __name__ == '__main__':
    db.create_all()
    app.debug = True
    app.run()
