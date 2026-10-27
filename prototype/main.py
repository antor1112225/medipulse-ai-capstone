"""
MediPulse AI - Console Demonstration & Interface Prototyping
Executes an end-to-end clinical workflow exercising at least 5 classes.
"""

from models import Patient, Doctor, Appointment, MedicalRecord, Prescription, TriageEngine
import json


def print_banner(title: str):
    print("\n" + "=" * 65)
    print(f"  {title.upper()}")
    print("=" * 65)


def run_demo():
    print_banner("MediPulse AI - Final Capstone Project Prototype")
    print("Initializing Core Clinical Subsystems & Domain Entities...\n")

    # 1. Instantiate AI Triage Engine
    triage_ai = TriageEngine(version="v2.1-ClinicalHeuristics")
    print(f"[Engine] Triage Engine initialized (Version: {triage_ai.version})")

    # 2. Instantiate Patient (Class 1)
    patient = Patient(
        user_id="PAT-10042",
        name="Khalid Mansoor",
        email="khalid.mansoor@university.edu",
        phone="+880-1711-234567",
        dob="1999-04-15",
        blood_group="O+",
        insurance_id="HLTH-INS-88992"
    )
    print(f"[Created Patient] ID: {patient.user_id} | Name: {patient.name} | Blood Group: {patient.blood_group}")

    # 3. Instantiate Doctors (Class 2)
    doctor_cardio = Doctor(
        user_id="DOC-902",
        name="Dr. Eleanor Vance, MD",
        email="e.vance@medipulse.org",
        phone="+1-555-019-2834",
        specialization="Cardiology",
        license_number="BMDC-MD-77291",
        consultationFee=120.00
    )
    doctor_gp = Doctor(
        user_id="DOC-903",
        name="Dr. Tariq Rahman, MBBS",
        email="t.rahman@medipulse.org",
        phone="+1-555-014-8831",
        specialization="General Practice",
        license_number="BMDC-GP-44120",
        consultationFee=50.00
    )
    print(f"[Created Doctor] {doctor_cardio.name} ({doctor_cardio.specialization})")
    print(f"[Created Doctor] {doctor_gp.name} ({doctor_gp.specialization})")

    # 4. Perform Clinical Symptom Triage (Class 6)
    print_banner("Step 1: Patient Symptom Submission & AI Triage")
    patient_complaint = "Experiencing acute chest pain and shortness of breath since morning."
    bp_reading = 165
    print(f"Patient Reported Symptoms: \"{patient_complaint}\"")
    print(f"Reported Systolic BP: {bp_reading} mmHg")

    triage_result = triage_ai.evaluate(symptoms=patient_complaint, systolic_bp=bp_reading)
    print("\n--- AI Triage Assessment ---")
    for k, v in triage_result.items():
        print(f"  * {k.replace('_', ' ').title()}: {v}")

    # 5. Schedule Appointment (Class 3)
    print_banner("Step 2: Intelligent Appointment Booking")
    assigned_doctor = doctor_cardio if triage_result["recommended_specialty"] == "Cardiology" else doctor_gp
    appointment = Appointment(
        appointment_id="APT-2026-9901",
        patient=patient,
        doctor=assigned_doctor,
        date_time="2026-10-28 10:30 AM",
        triage_priority=triage_result["acuity"]
    )
    print(f"Appointment Created Successfully: {appointment.appointment_id}")
    print(f"Patient: {appointment.patient.name}")
    print(f"Assigned Specialist: {appointment.doctor.name} ({appointment.doctor.specialization})")
    print(f"Scheduled Slot: {appointment.date_time}")
    print(f"Acuity Level: {appointment.triage_priority}")
    print(f"Status: {appointment.status}")

    # 6. Doctor Consultation & Electronic Health Record Creation (Class 4)
    print_banner("Step 3: Clinical Consultation & EHR Documentation")
    print(f"Dr. {appointment.doctor.name} is conducting the consultation session...")
    
    ehr_record = appointment.doctor.conduct_consultation(
        appointment=appointment,
        diagnosis="Stage 2 Hypertension with Angina Pectoris Symptoms",
        vitals={"BP": "162/98 mmHg", "HeartRate": "92 bpm", "SpO2": "97%", "Temp": "98.4 F"},
        treatment_plan="Immediate lifestyle sodium restriction, calcium channel blocker therapy, and stress reduction."
    )
    print("\n[Electronic Health Record Generated]")
    print(f"  * Record ID: {ehr_record.record_id}")
    print(f"  * Diagnosis: {ehr_record.diagnosis}")
    print(f"  * Recorded Vitals: {ehr_record.vitals}")
    print(f"  * Treatment Plan: {ehr_record.treatment_plan}")
    print(f"  * Appointment Status Updated: {appointment.status}")

    # 7. Issue Digital Prescription (Class 5)
    print_banner("Step 4: Digital Prescription Formulation")
    rx_medications = [
        {"medicine": "Amlodipine Besylate", "dosage": "5 mg", "route": "Oral", "frequency": "Once daily morning", "duration": "30 days"},
        {"medicine": "Sublingual Nitroglycerin", "dosage": "0.4 mg", "route": "Sublingual", "frequency": "PRN for acute chest discomfort", "duration": "As needed"}
    ]
    instructions = "Take medication with water. Avoid heavy sodium meals. Return to ER if chest pressure radiates to arm."

    prescription = appointment.doctor.issue_prescription(
        appointment=appointment,
        medications=rx_medications,
        instructions=instructions
    )
    print(f"[Prescription Formatted] ID: {prescription.prescription_id}")
    print(f"Doctor Signature: {prescription.doctor.name} ({prescription.doctor.license_number})")
    print("Prescribed Medications:")
    for idx, med in enumerate(prescription.medications, 1):
        print(f"  {idx}. {med['medicine']} - {med['dosage']} [{med['frequency']}] ({med['duration']})")
    print(f"Clinical Guidance: {prescription.instructions}")

    # 8. Verification of Patient Health Records
    print_banner("Step 5: Patient EHR Summary & Verification")
    summary = patient.get_dashboard_summary()
    for k, v in summary.items():
        print(f"  {k}: {v}")

    print("\n" + "=" * 65)
    print("  PROTOTYPE DEMONSTRATION COMPLETE: 6 CLASSES VERIFIED")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    run_demo()