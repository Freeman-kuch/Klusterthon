from kluster import db
from kluster.models.base import BaseModel
from kluster.models.users import Users
from datetime import datetime




class Profiles(BaseModel):
    """Profiles model"""
    __tablename__ = 'profiles'

    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), unique=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=True)
    gender = db.Column(db.Enum(
        'male',
        'female',
        name="GENDER",
    ),
        nullable=True
    )
    blood_group = db.Column(db.Enum(
        'A',
        'B',
        'O',
        'AB',
        'others',
        name="BLOOD_GROUP",
    ),
        nullable=True
    )
    address = db.Column(db.String(100), nullable=True)
    allergies = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    display_picture = db.Column(db.String(255), nullable=True)

    # user = db.relationship("users", backref=db.backref("profiles", lazy=True), cascade="all, delete")

    def __init__(
            self,
            user_id: str,
            first_name: str,
            last_name: str,
            date_of_birth: str = None,
            gender: str = None,
            address: str = None,
            display_picture: str = None,
            blood_group: str = None,
            allergies: str = None,
            age : int = None
            ):
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
        self.allergies = allergies
        self.age = age
        self.blood_group = blood_group
        self.address = address
        self.display_picture = display_picture

    def __repr__(self):
        """Representation of Profiles model"""
        return (f"<Profiles(id={self.id}, "
                f"user_id={self.user_id}, "
                f"first_name={self.first_name},"
                f"last_name={self.last_name}, "
                f"gender={self.gender}, "
                f"address={self.address}, "
                f"display_picture = {self.display_picture},"
                f"blood_group= {self.blood_group},"
                f"age={self.age},"
                f"allergies={self.allergies})>")

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
