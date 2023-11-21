from kluster import db
from kluster.models.base import BaseModel


class Medication(BaseModel):
    __tablename__ = "medication"