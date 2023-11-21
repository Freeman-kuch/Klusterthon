from kluster.models.base import BaseModel
from kluster import db


class Roles(BaseModel):
    """Role Model :)"""
    __tablename__ = "roles"
    role = db.Column(db.Enum('doctor', 'patient', name="USER_ROLE"), nullable=False)  # noqa E501
    # relationships specification
    permissions = db.relationship("Permissions", backref=db.backref("role", lazy=True),  # noqa E501
                                  cascade="all, delete-orphan")
    users = db.relationship("Users", backref=db.backref("role", lazy=True),
                            cascade="all, delete-orphan")

    def __init__(self, role):
        """object constructor"""
        super().__init__()
        self.role = role

    def __repr__(self):
        """official object representation"""
        return {
            "id": self.id,
            "role": self.role,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def format(self):
        """Format the object's attributes as a dictionary"""
        return {
            "id": self.id,
            "role": self.role,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
