from kluster import db
from kluster.models.base import BaseModel
from kluster.models.users import Users


class Medication(BaseModel):
    __tablename__ = "medications"
    name = db.Column(db.String(255), nullable=False)
    patient_id = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False, unique=True,)
    prescribed_by = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False, unique=True,)
    dosage = db.Column(db.Enum(
        "daily",
        "bi_daily",
        "tri_daily",
        "quad_daily",
        name="FREQUENCY"
    ),
        nullable=False
    )
    description = db.Column(db.String(255), nullable=True)
    has_taken = db.Column(db.Boolean(255), nullable=True)
    start_date = db.Column(db.DateTime(), nullable=False)
    end_date = db.Column(db.DateTime(), nullable=False)

    user = db.relationship("users", backref=db.backref("medications", lazy=True), cascade="all, delete-orphan")