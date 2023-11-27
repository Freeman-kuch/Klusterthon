# from datetime import datetime, timedelta
# from kluster.models.medication import Medication
# from kluster.models.medication_logs import MedicationLogs  
# from kluster.helpers import query_one_filtered  

# #@celery.task
# def create_medication_logs_async(user_id, medication_id):
#     medication = query_one_filtered(Medication, id=medication_id, patient_id=user_id)

#     if not medication:
#         # If the medication is not found, you can either log this or handle it as needed
#         return 'Medication not found'

#     dosage = {
#         "daily": 1,
#         "bi_daily": 2,
#         "tri_daily": 3,
#         "quad_daily": 4,
#     }

#     medication_start = medication.start_date
#     duration = medication.end_date - medication_start

#     for day in range(duration.days + 1):  # +1 to include the end date
#         day_date = medication_start + timedelta(days=day)
#         for dose in range(dosage.get(medication.dosage, 1)):
#             time_increment = timedelta(hours=24 / dosage.get(medication.dosage, 1))
#             scheduled_time = datetime.combine(day_date, datetime.min.time()) + dose * time_increment

#             # Create and save MedicationLog entry
#             MedicationLogs(user_id=user_id, medication_id=medication.id, scheduled_time=scheduled_time).insert()

#     return 'Medication logs scheduled successfully'


















# from flask import Blueprint, request, jsonify, redirect, url_for
# from datetime import datetime, timedelta

# from kluster import jwt
# from kluster.helpers import convert_pic_to_link, query_one_filtered
# from kluster.models.medication import Medication
# from kluster.models.medication_logs import MedicationLogs
# from kluster.models.roles import Roles
# from kluster.models.users import Users

# medicationlogs_bp = Blueprint("medication_logs", __name__, url_prefix="/api/v1/medicationlogs")

# # I NEED A FUNCTION THAT WILL POPULATE THE MEDICATION LOGS TABLE BASED ON THE START AND END TIME OF A DRUG,
# # THE FREQUENCY OF THE DRUG AND THE TIME TAKEN

# dosage = {
#     "daily": 1,
#     "bi_daily": 2,
#     "tri_daily": 3,
#     "quad_daily": 4,
# }


# @medicationlogs_bp.route("/<string:user_id>/<string:med_id>", methods=["GET"])
# def schedule_medication_logs(user_id, med_id):
#     medication = query_one_filtered(Medication, id=med_id, patient_id=user_id)

#     if not medication:
#         return jsonify({'error': 'Medication not found'}), 404

#     medication_start = medication.start_date
#     duration = medication.end_date - medication_start

#     for day in range(duration.days + 1):  # +1 to include the end date
#         day_date = medication_start + timedelta(days=day)
#         for dose in range(dosage.get(medication.dosage, 1)):
#             time_increment = timedelta(hours=24 / dosage.get(medication.dosage, 1))
#             scheduled_time = datetime.combine(day_date, datetime.min.time()) + dose * time_increment

#             # Create and save MedicationLog entry
#             MedicationLogs(user_id=user_id, medication_id=medication.id, scheduled_time=scheduled_time).insert()

#     return jsonify({'message': 'Medication logs scheduled successfully'}), 200


# #CREATING A MEDICATION FILTER LOG FOR PATIENTS AND DOCTORS

# #FIRST I SHOULD QUERY THE DB FOR THE USRE ID
# #IF THERE IS NO QUERY PARAM, DEFAULTY I SHOULD RETURN FOR JUST ONE DAY
# #IF THERE IS A PARAM (1 DAY, 1 WEEK, 1 MONTH)
