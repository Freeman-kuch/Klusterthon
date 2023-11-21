from kluster import db
from kluster.models.base import BaseModel


class Users(BaseModel):
    """Users model for the users table"""
    __tablename__ = "users"
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.String(255), db.ForeignKey("roles.id"),
                        nullable=False, unique=True)
    refresh_token = db.Column(db.String(255), nullable=False)
    access_token = db.Column(db.String(255), nullable=False)
    # relationships specification
    profile = db.relationship("Profile", backref=db.backref("user", lazy=True),
                              cascade="all, delete-orphan")

    def __init__(self, email: str, password: str, role_id: str,
                 refresh_token: str = None, access_token: str = None):
        super().__init__()
        self.email = email
        self.password = password
        self.role_id = role_id
        self.refresh_token = refresh_token
        self.access_token = access_token

    def __repr__(self):
        return {
            "id": self.id,
            "email": self.email,
            "role_id": self.role_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def format(self):
        return {
            "id": self.id,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
