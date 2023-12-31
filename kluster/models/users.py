from kluster import db
from kluster.models.base import BaseModel
from kluster.models.profiles import Profiles


class Users(BaseModel):
    """Users model for the users table"""
    __tablename__ = "users"
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=True)
    role_id = db.Column(db.String(255), db.ForeignKey("roles.id"),
                        nullable=True, unique=True)
    refresh_token = db.Column(db.String(400), nullable=True)
    access_token = db.Column(db.String(400), nullable=True)
    google_refresh_token = db.Column(db.String(400), nullable=True)
    google_access_token = db.Column(db.String(400), nullable=True)

    # relationships specification
    profile = db.relationship("Profiles", backref=db.backref("users", lazy=True), cascade="all, delete-orphan")

    def __init__(self, email: str, password: str,
                 refresh_token: str = None, access_token: str = None, role_id: str = None, **kwargs):
        super().__init__()
        self.email = email
        self.password = password
        self.role_id = role_id
        self.refresh_token = refresh_token
        self.access_token = access_token
        if user_id := kwargs.get("id", None):
            self.id = user_id

    def __repr__(self):
        return (f"<User(id={self.id}, email={self.email}, role_id={self.role_id}, created_at={self.created_at}, "
                f"updated_at={self.updated_at})>")

    def format(self):
        return {
            "id": self.id,
            "email": self.email,
            "created_at": self.created_at,
            "role_id": self.role_id,
            "updated_at": self.updated_at,
        }

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "role_id": self.role_id if self.role_id else None,
            "refresh_token": self.refresh_token,
            "access_token": self.access_token,
            "google_refresh_token": self.google_refresh_token if self.google_refresh_token else None,
            "google_access_token": self.google_access_token if self.google_access_token else None,
        }
