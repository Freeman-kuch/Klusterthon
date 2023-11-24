from kluster import db
from kluster.models.base import BaseModel
from kluster.models.users import Users


class Medication(BaseModel):
    __tablename__ = "medications"
    name = db.Column(db.String(255), nullable=False)
    patient_id = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False, unique=True, )
    prescribed_by = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False, unique=True, )
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

    # user = db.relationship("Users", backref=db.backref("Medications", lazy=True), cascade="all, delete-orphan")

    user = db.relationship("Users", foreign_keys="[Medication.patient_id]",
                           backref=db.backref("medications_patient", lazy="dynamic"), cascade="all, delete-orphan", single_parent=True)
    prescribed_by_user = db.relationship("Users", foreign_keys="[Medication.prescribed_by]",
                                         backref=db.backref("medications_prescribed", lazy="dynamic"),
                                         cascade="all, delete-orphan", single_parent=True)
