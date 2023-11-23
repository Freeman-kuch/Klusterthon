from kluster import db
from kluster.models.base import BaseModel
class MedicationLogs(BaseModel):
    __tablename__ = 'medication_logs'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    medication_id = db.Column(db.Integer, db.ForeignKey('medications.id'))
    
