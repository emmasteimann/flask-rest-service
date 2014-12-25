from app import db
from models import *

try:
    db.session.query(User).delete()
    db.session.query(UserGroup).delete()
    db.session.query(Group).delete()
    db.session.commit()
except:
    db.session.rollback()
