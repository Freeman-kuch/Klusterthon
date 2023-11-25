from kluster import db
from datetime import datetime
from kluster.models.base import BaseModel
from kluster.models.users import Users


class Medication(BaseModel):
    __tablename__ = "medications"
    name = db.Column(db.String(255), nullable=False)
    patient_id = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False, unique=False, )
    prescribed_by = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False, unique=False, )
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
    has_taken = db.Column(db.Boolean(255), nullable=False, default=False)
    start_date = db.Column(db.DateTime(), nullable=False)
    end_date = db.Column(db.DateTime(), nullable=False)

    user = db.relationship("Users", foreign_keys="[Medication.patient_id]",
                           backref=db.backref("medications_patient", lazy="dynamic"), cascade="all, delete-orphan",
                           single_parent=True)
    prescribed_by_user = db.relationship("Users", foreign_keys="[Medication.prescribed_by]",
                                         backref=db.backref("medications_prescribed", lazy="dynamic"),
                                         cascade="all, delete-orphan", single_parent=True)

    def __init__(self, name: str, patient_id: str, prescribed_by: str, dosage: str, start_date: datetime,
                 end_date: datetime, description: str = None, has_taken: bool = False):
        super().__init__()
        self.name = name
        self.patient_id = patient_id
        self.prescribed_by = prescribed_by
        self.dosage = dosage
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.has_taken = has_taken

    def __repr__(self):
        return (
            f"<Medication(id={self.id}, "
            f"name={self.name}, "
            f"patient_id={self.patient_id}, "
            f"prescribed_by_at={self.prescribed_by},"
            f"dosage={self.dosage},"
            f"start_date={self.start_date}"
            f"end_date={self.end_date})>")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "patient_id": self.patient_id,
            "prescribed_by": self.prescribed_by,
            "dosage": self.dosage,
            "description": self.description,
            "has_taken": self.has_taken,
            "start_date": self.start_date.strftime("%Y-%m-%d") if self.start_date else None,
            "end_date": self.end_date.strftime("%Y-%m-%d") if self.end_date else None,
        }

    def format(self):
        return {
            " name": self.name,
            "patient_id": self.patient_id,
            "prescribed_by": self.prescribed_by,
            "dosage": self.dosage,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "has_taken": self.has_taken,
        }
