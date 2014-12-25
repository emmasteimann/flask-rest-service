from app import db
from models import *

new_user = User("emma", "steimann", "esteimann")
new_group = Group("fancy_people")
db.session.add(new_user)
db.session.add(new_group)
db.session.add(UserGroup(new_user, new_group))
db.session.commit()
