from kluster.models.base import BaseModel
from kluster import db
from kluster.models.users import Users
from kluster.models.roles import Roles


class Permissions(BaseModel):
    """Role Model permissions :)"""
    __tablename__ = "permissions"
    permission = db.Column(db.Enum('doctor', 'patient', name="USER_ROLE"),
                           nullable=False)
    role_id = db.Column(db.String(60), db.ForeignKey("users.id"))
    Roles = db.relationship("Roles", backref=db.backref("Permissions", lazy=True),  # noqa E501
                                  cascade="all, delete-orphan")

    def __init__(self, permission, role_id):
        """Initialize Profiles model

            Args:
                permission (str): Permissions for roles
                role_id (string): foreignkey to the role
        """
        super().__init__()
        self.permission = permission
        self.role_id = role_id

    def __repr__(self):
        """official object representation"""
        return {
            "id": self.id,
            "self.permission": self.permission,
            "role_id": self.role_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def format(self):
        """Format the object's attributes as a dictionary"""
        return {
            "id": self.id,
            "self.permission": self.permission,
            "role_id": self.role_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
