"""
MediPulse AI - Core Object-Oriented Domain Models
Capstone Project Prototype Implementation
Demonstrating at least 5 interconnected UML classes.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Optional
import uuid


class User(ABC):
    """
    Abstract Base Class representing a platform user in the healthcare system.
    Demonstrates OOP Inheritance, Encapsulation, and Abstraction.
    """
    def __init__(self, user_id: str, name: str, email: str, phone: str, role: str):
        self._user_id: str = user_id
        self._name: str = name
        self._email: str = email
        self._phone: str = phone
        self._role: str = role
        self._created_at: datetime = datetime.now()
        self._is_active: bool = True

    # Getters and Setters (Encapsulation)
    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value

    @property
    def email(self) -> str:
        return self._email

    @property
    def phone(self) -> str:
        return self._phone

    @property
    def role(self) -> str:
        return self._role

    @property
    def is_active(self) -> bool:
        return self._is_active

    @abstractmethod
    def get_dashboard_summary(self) -> Dict[str, str]:
        """Abstract method to be implemented by concrete user roles."""
        pass

    def to_dict(self) -> Dict:
        return {
            "user_id": self._user_id,
            "name": self._name,
            "email": self._email,
            "phone": self._phone,
            "role": self._role,
            "is_active": self._is_active
        }


class Patient(User):
    """
    Class 1: Patient Entity inheriting from User.
    Represents individuals receiving healthcare services.
    """
    def __init__(self, user_id: str, name: str, email: str, phone: str, 
                 dob: str, blood_group: str, insurance_id: str):
        super().__init__(user_id, name, email, phone, role="PATIENT")
        self.dob: str = dob
        self.blood_group: str = blood_group
        self.insurance_id: str = insurance_id
        self.medical_records: List['MedicalRecord'] = []
        self.prescriptions: List['Prescription'] = []

    def get_dashboard_summary(self) -> Dict[str, str]:
        return {
            "User Type": "Patient",
            "Name": self.name,
            "Blood Group": self.blood_group,
            "Total Records": str(len(self.medical_records)),
            "Active Prescriptions": str(len(self.prescriptions))
        }

    def add_record(self, record: 'MedicalRecord') -> None:
        self.medical_records.append(record)

    def add_prescription(self, rx: 'Prescription') -> None:
        self.prescriptions.append(rx)

    def to_dict(self) -> Dict:
        base = super().to_dict()
        base.update({
            "dob": self.dob,
            "blood_group": self.blood_group,
            "insurance_id": self.insurance_id,
            "record_count": len(self.medical_records),
            "prescription_count": len(self.prescriptions)
        })
        return base


class Doctor(User):
    """
    Class 2: Doctor / Physician Entity inheriting from User.
    Represents healthcare providers conducting consultations and issuing treatments.
    """
    def __init__(self, user_id: str, name: str, email: str, phone: str,
                 specialization: str, license_number: str, consultation_fee: float):
        super().__init__(user_id, name, email, phone, role="DOCTOR")
        self.specialization: str = specialization
        self.license_number: str = license_number
        self.consultation_fee: float = consultation_fee
        self.scheduled_appointments: List['Appointment'] = []
        self.is_available: bool = True

    def get_dashboard_summary(self) -> Dict[str, str]:
        return {
            "User Type": "Physician",
            "Name": self.name,
            "Specialization": self.specialization,
            "License": self.license_number,
            "Consultation Fee": f"${self.consultation_fee:.2f}",
            "Scheduled Consultations": str(len(self.scheduled_appointments))
        }

    def conduct_consultation(self, appointment: 'Appointment', diagnosis: str, 
                             vitals: Dict[str, str], treatment_plan: str) -> 'MedicalRecord':
        """
        Creates a permanent EHR record and links it to the patient.
        """
        record_id = f"MR-{uuid.uuid4().hex[:6].upper()}"
        record = MedicalRecord(
            record_id=record_id,
            patient=appointment.patient,
            doctor=self,
            diagnosis=diagnosis,
            vitals=vitals,
            treatment_plan=treatment_plan
        )
        appointment.patient.add_record(record)
        appointment.complete()
        return record

    def issue_prescription(self, appointment: 'Appointment', medications: List[Dict[str, str]], 
                           instructions: str) -> 'Prescription':
        """
        Generates and signs a digital prescription.
        """
        rx_id = f"RX-{uuid.uuid4().hex[:6].upper()}"
        rx = Prescription(
            prescription_id=rx_id,
            appointment_id=appointment.appointment_id,
            patient=appointment.patient,
            doctor=self,
            medications=medications,
            instructions=instructions
        )
        appointment.patient.add_prescription(rx)
        return rx


class Appointment:
    """
    Class 3: Appointment Entity managing clinical encounters.
    Demonstrates Association between Patient and Doctor.
    """
    STATUS_SCHEDULED = "SCHEDULED"
    STATUS_IN_PROGRESS = "IN_PROGRESS"
    STATUS_COMPLETED = "COMPLETED"
    STATUS_CANCELLED = "CANCELLED"

    def __init__(self, appointment_id: str, patient: Patient, doctor: Doctor, 
                 date_time: str, triage_priority: str = "ROUTINE"):
        self.appointment_id: str = appointment_id
        self.patient: Patient = patient
        self.doctor: Doctor = doctor
        self.date_time: str = date_time
        self.triage_priority: str = triage_priority  # CRITICAL, URGENT, ROUTINE
        self.status: str = self.STATUS_SCHEDULED
        self.doctor.scheduled_appointments.append(self)

    def reschedule(self, new_date_time: str) -> None:
        if self.status == self.STATUS_COMPLETED:
            raise ValueError("Cannot reschedule a completed appointment.")
        self.date_time = new_date_time

    def cancel(self) -> None:
        self.status = self.STATUS_CANCELLED

    def complete(self) -> None:
        self.status = self.STATUS_COMPLETED

    def to_dict(self) -> Dict:
        return {
            "appointment_id": self.appointment_id,
            "patient_name": self.patient.name,
            "doctor_name": self.doctor.name,
            "doctor_specialty": self.doctor.specialization,
            "date_time": self.date_time,
            "triage_priority": self.triage_priority,
            "status": self.status
        }


class MedicalRecord:
    """
    Class 4: Electronic Health Record (EHR) entry.
    Encapsulates patient clinical encounters, diagnostics, and vitals.
    """
    def __init__(self, record_id: str, patient: Patient, doctor: Doctor, 
                 diagnosis: str, vitals: Dict[str, str], treatment_plan: str):
        self.record_id: str = record_id
        self.patient: Patient = patient
        self.doctor: Doctor = doctor
        self.diagnosis: str = diagnosis
        self.vitals: Dict[str, str] = vitals  # e.g. {"BP": "120/80", "Pulse": "72", "Temp": "98.6F"}
        self.treatment_plan: str = treatment_plan
        self.created_at: datetime = datetime.now()

    def to_dict(self) -> Dict:
        return {
            "record_id": self.record_id,
            "patient_name": self.patient.name,
            "doctor_name": self.doctor.name,
            "diagnosis": self.diagnosis,
            "vitals": self.vitals,
            "treatment_plan": self.treatment_plan,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }


class Prescription:
    """
    Class 5: Digital Prescription entity.
    Maintains medication orders, dosage, route, instructions, and fulfillment status.
    """
    def __init__(self, prescription_id: str, appointment_id: str, patient: Patient, 
                 doctor: Doctor, medications: List[Dict[str, str]], instructions: str):
        self.prescription_id: str = prescription_id
        self.appointment_id: str = appointment_id
        self.patient: Patient = patient
        self.doctor: Doctor = doctor
        self.medications: List[Dict[str, str]] = medications
        self.instructions: str = instructions
        self.is_dispensed: bool = False
        self.created_at: datetime = datetime.now()

    def dispense(self) -> None:
        self.is_dispensed = True

    def to_dict(self) -> Dict:
        return {
            "prescription_id": self.prescription_id,
            "appointment_id": self.appointment_id,
            "patient_name": self.patient.name,
            "doctor_name": self.doctor.name,
            "medications": self.medications,
            "instructions": self.instructions,
            "is_dispensed": self.is_dispensed,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }


class TriageEngine:
    """
    Class 6 (Bonus): Clinical Decision Support & Symptom Triage Classifier.
    Evaluates reported symptoms and vital signs to assign acuity ratings.
    """
    def __init__(self, version: str = "v1.2.0-clinical"):
        self.version: str = version
        self._rules = {
            "chest pain": ("CRITICAL", "Cardiology"),
            "shortness of breath": ("CRITICAL", "Pulmonology"),
            "high fever": ("URGENT", "Internal Medicine"),
            "severe headache": ("URGENT", "Neurology"),
            "fracture suspicion": ("URGENT", "Orthopedics"),
            "skin rash": ("ROUTINE", "Dermatology"),
            "mild cough": ("ROUTINE", "General Practice")
        }

    def evaluate(self, symptoms: str, systolic_bp: Optional[int] = None) -> Dict[str, str]:
        symptoms_lower = symptoms.lower()
        acuity = "ROUTINE"
        specialist = "General Practice"
        score = 10

        for keyword, (level, rec_dept) in self._rules.items():
            if keyword in symptoms_lower:
                if level == "CRITICAL":
                    acuity = "CRITICAL"
                    specialist = rec_dept
                    score = 95
                    break
                elif level == "URGENT" and acuity != "CRITICAL":
                    acuity = "URGENT"
                    specialist = rec_dept
                    score = 65

        # Physiological vitals safety override
        if systolic_bp and systolic_bp >= 180:
            acuity = "CRITICAL"
            specialist = "Cardiology"
            score = 99

        return {
            "acuity": acuity,
            "recommended_specialty": specialist,
            "triage_score": f"{score}/100",
            "engine_version": self.version,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
