from kluster import db
from kluster.models.base import BaseModel


class Users(BaseModel):
    __tablename__ = "users"
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.String(255), nullable=False, unique=True)
    refresh_token = db.Column(db.String(255), nullable=False)
    access_token = db.Column(db.String(255), nullable=False)

    def __init__(self, email, password, role_id, refresh_token, access_token):
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
            "refresh_token": self.refresh_token,
            "access_token": self.access_token,
            "role_id": self.role_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def format(self):
        return {
            "id": self.id,
            "email": self.email,
            "refresh_token": self.refresh_token,
            "access_token": self.access_token,
            "role_id": self.role_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
