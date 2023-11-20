from kluster import db
from kluster.models.base import BaseModel

class Profiles(BaseModel):
    """Profiles model"""
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    date_of_birth = db.Column(db.DateTime)
    gender= db.Column(db.Enum('male', 'female', 'undefined',
                            name="GENDER"), server_default="undefined", nullable=False)
    address = db.Column(db.String(100))
    display_picture = db.Column(db.String(100))
