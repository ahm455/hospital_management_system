def patient_appts(patient_id):
    return f"patient_appts:{patient_id}"

def patient_prescriptions(patient_id):
    return f"patient_prescriptions:{patient_id}"

def patient_labs(patient_id):
    return f"patient_labs:{patient_id}"

def doctor_appts(doctor_id, date):
    return f"doctor_appts:{doctor_id}:{date}"

def patient_vitals(patient_id):
    return f"patient_vitals:{patient_id}"