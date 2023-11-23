from kluster import db
from kluster.models.base import BaseModel
from kluster.models.users import Users
from datetime import datetime




class Profiles(BaseModel):
    """Profiles model"""
    __tablename__ = 'profiles'

    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    date_of_birth = db.Column(db.DateTime)
    gender = db.Column(db.Enum(
        'male',
        'female',
        name="GENDER",
    ),
        nullable=False
    )
    blood_group = db.Column(db.Enum(
        'A',
        'B',
        'O',
        'AB',
        'others',
        name="BLOOD_GROUP",
    ),
        nullable=False
    )
    address = db.Column(db.String(100))
    allergies = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, nullable=False)
    display_picture = db.Column(db.String(255))

    user = db.relationship("users", backref=db.backref("profiles", lazy=True), cascade="all, delete")

    def __init__(self, user_id: str, first_name: str, last_name: str,
                 date_of_birth: str, gender: str, address: str = None,
                 display_picture: str = None):
        """Initialize Profiles model

        Args:
            user_id (str): user id
            first_name (str): The first name of the user
            last_name (str): The last name of the user
            date_of_birth (datetime): The date of birth of the user.
            gender (enum): The gender of the user.
            address (str): The address of the user.
            display_picture (str): The display picture of the user.
        """
        super().__init__()
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.address = address
        self.display_picture = display_picture

    def __repr__(self):
        """Representation of Profiles model"""
        return f"<Profiles(id={self.id}, user_id={self.user_id}, first_name={self.first_name}, last_name={self.last_name}, gender={self.gender}, address={self.address}, display_picture = {self.display_picture})>"

    def format(self):
        """Format the object's attributes as a dictionary"""
        return ({
            "id": self.id,
            "user_id": self.user_id_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "gender": self.gender,
            "address": self.address,
            "display_picture": self.display_picture
        })
