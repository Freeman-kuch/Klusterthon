from kluster.models.base import BaseModel
from kluster import db


class Roles(BaseModel):
    __tablename__ = "roles"
    role = db.Column(db.Enum('doctor', 'patient', name="USER_ROLE"), nullable=False)

    def __init__(self, role):
        """object constructor"""
        super().__init__()
        self.role = role

    def __repr__(self):
        """official object representation"""
        return {
            "id": self.id,
            "role": self.role,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
        }

    def format(self):
        """Format the object's attributes as a dictionary"""
        return {
            "id": self.id,
            "role": self.role,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
        }
