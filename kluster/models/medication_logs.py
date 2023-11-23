from kluster import db
from kluster.models.base import BaseModel
from kluster.models.users import Users
from kluster.models.medication import Medication
import datetime


class MedicationLogs(BaseModel):
    __tablename__ = 'medication_logs'
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'))
    medication_id = db.Column(db.String(60), db.ForeignKey('medication.id'))
    time_taken = db.Column(db.DateTime, nullable=False)
    taken_status = db.Column(db.Boolean, nullable=False)
    scheduled_time = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.String(255), nullable=True)
    reminder_sent = db.Column(db.Boolean, nullable=False, default=False)
    acknowledged = db.Column(db.Boolean, nullable=False, default=False)

    user = db.relationship("users", backref=db.backref("medication_logs", lazy=True), cascade="all, delete-orphan")
    medication = db.relationship("medication", backref=db.backref("medication_logs", lazy=True),
                                 cascade="all, delete-orphan")

    # we already have dosage for this stiil need?
    # quantity_taken = db.Column(db.Float, nullable=True)

    def __init__(self, user_id: int, medication_id: int, time_taken: datetime, taken_status: bool,
                 scheduled_time: datetime, notes: str = None, reminder_sent: bool = False, acknowledged: bool = False):
        super().__init__()
        self.user_id = user_id
        self.medication_id = medication_id
        self.time_taken = time_taken
        self.taken_status = taken_status
        self.scheduled_time = scheduled_time
        self.notes = notes
        self.reminder_sent = reminder_sent
        self.acknowledged = acknowledged

    def __repr__(self):
        return f"<MedicationLogs(id= {self.id} user_id={self.user_id}, medication_id={self.medication_id}, time_taken={self.time_taken}, taken_status={self.taken_status}, scheduled_time={self.scheduled_time}, notes={self.notes}, reminder_sent={self.reminder_sent}, acknowledged={self.acknowledged})>"

    def format(self):
        """Format the object's attributes as a dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'medication_id': self.medication_id,
            'time_taken': self.time_taken,
            'taken_status': self.taken_status,
            'scheduled_time': self.scheduled_time,
            'notes': self.notes,
            'reminder_sent': self.reminder_sent,
            'acknowledged': self.acknowledged
        }
