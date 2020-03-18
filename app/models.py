from app import app


#base model for other database tables to inherit
class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.integer, primary_key = True)
    date_created = db.Column(db.DateTime, default = db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default = db.func.current_timestamp(), onupdate=db.func.current_timestamp())


#dbobject
class Number(Base):

    __tablename__ = 'phone_number'

    blacklist_number =db.Column(db.String(), nullable =False)
    talkdesk_number = db.Column(db.String(), nullable =False)

    def __init__(self, number1, number2):
        self.blacklist_number = number1
        self.talkdesk_number = number2
