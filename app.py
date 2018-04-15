from __future__ import print_function
from comtoken import app,db
from flask_script import Manager
from urllib.parse import urljoin

manager = Manager(app)

@manager.command
def init_db():
    db.create_all()

if __name__ == '__main__':
    manager.run()
