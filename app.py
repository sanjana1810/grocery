from flask import Flask
from applications.database import db

app=Flask(__name__)
app.config['SECRET_KEY']= 'thisisyoursecretkey'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.sqlite3'
UPLOAD_FOLDER='static'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS']=('png','jpg', 'jpeg', 'gif')
db.init_app(app)

app.app_context().push()
db.create_all()
from applications.controllers import *

if __name__=='__main__':
    app.run(debug=True)