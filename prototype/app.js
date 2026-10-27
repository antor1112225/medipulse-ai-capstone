/**
 * MediPulse AI - Object-Oriented Frontend Controller
 * Direct implementation of the 5 UML classes in JavaScript:
 * Class 1: Patient (extends User)
 * Class 2: Doctor (extends User)
 * Class 3: Appointment
 * Class 4: MedicalRecord
 * Class 5: Prescription
 * Class 6: TriageEngine
 */

class User {
  constructor(userId, name, email, phone, role) {
    this.userId = userId;
    this.name = name;
    this.email = email;
    this.phone = phone;
    this.role = role;
  }
}

class Patient extends User {
  constructor(userId, name, email, phone, dob, bloodGroup, insuranceId) {
    super(userId, name, email, phone, 'PATIENT');
    this.dob = dob;
    this.bloodGroup = bloodGroup;
    this.insuranceId = insuranceId;
    this.records = [];
    this.prescriptions = [];
  }
}

class Doctor extends User {
  constructor(userId, name, email, phone, specialization, licenseNumber, consultationFee) {
    super(userId, name, email, phone, 'DOCTOR');
    this.specialization = specialization;
    this.licenseNumber = licenseNumber;
    this.consultationFee = consultationFee;
  }
}

class Appointment {
  constructor(appointmentId, patient, doctor, dateTime, triagePriority = 'ROUTINE') {
    this.appointmentId = appointmentId;
    this.patient = patient;
    this.doctor = doctor;
    this.dateTime = dateTime;
    this.triagePriority = triagePriority;
    this.status = 'SCHEDULED';
  }

  complete() {
    this.status = 'COMPLETED';
  }
}

class MedicalRecord {
  constructor(recordId, patientId, doctorId, diagnosis, vitals, treatmentPlan) {
    this.recordId = recordId;
    this.patientId = patientId;
    this.doctorId = doctorId;
    this.diagnosis = diagnosis;
    this.vitals = vitals;
    this.treatmentPlan = treatmentPlan;
    this.timestamp = new Date().toLocaleString();
  }
}

class Prescription {
  constructor(prescriptionId, appointmentId, patientName, doctorName, medications, instructions) {
    this.prescriptionId = prescriptionId;
    this.appointmentId = appointmentId;
    this.patientName = patientName;
    this.doctorName = doctorName;
    this.medications = medications;
    this.instructions = instructions;
    this.issuedAt = new Date().toLocaleString();
  }
}

class TriageEngine {
  constructor() {
    this.version = 'v2.1-SmartHeuristics';
  }

  evaluate(symptoms, systolicBp) {
    const text = symptoms.toLowerCase();
    let acuity = 'ROUTINE';
    let specialty = 'General Practice';
    let urgencyScore = 15;

    if (text.includes('chest pain') || text.includes('heart') || (systolicBp && systolicBp >= 170)) {
      acuity = 'CRITICAL';
      specialty = 'Cardiology';
      urgencyScore = 95;
    } else if (text.includes('breath') || text.includes('lungs')) {
      acuity = 'CRITICAL';
      specialty = 'Pulmonology';
      urgencyScore = 90;
    } else if (text.includes('fever') || text.includes('infection') || text.includes('vomit')) {
      acuity = 'URGENT';
      specialty = 'Internal Medicine';
      urgencyScore = 65;
    } else if (text.includes('bone') || text.includes('fracture') || text.includes('joint')) {
      acuity = 'URGENT';
      specialty = 'Orthopedics';
      urgencyScore = 60;
    }

    return {
      acuity,
      specialty,
      urgencyScore,
      evaluatedAt: new Date().toLocaleTimeString()
    };
  }
}

// ----------------- SYSTEM STATE & RUNTIME DATA -----------------
const triageEngine = new TriageEngine();

const doctors = [
  new Doctor('DOC-01', 'Dr. Eleanor Vance, MD', 'e.vance@medipulse.org', '+1-555-0192', 'Cardiology', 'BMDC-7712', 120),
  new Doctor('DOC-02', 'Dr. Tariq Rahman, MBBS', 't.rahman@medipulse.org', '+1-555-0148', 'General Practice', 'BMDC-4412', 50),
  new Doctor('DOC-03', 'Dr. Sarah Jenkins, MD', 's.jenkins@medipulse.org', '+1-555-0821', 'Pulmonology', 'BMDC-9921', 110)
];

let currentPatient = new Patient(
  'PAT-101',
  'Khalid Mansoor',
  'khalid@university.edu',
  '+880-1711-234567',
  '1999-05-14',
  'O+',
  'INS-BD-8891'
);

const appointments = [];
const records = [];
const prescriptions = [];

// ----------------- DOM INITIALIZATION & EVENTS -----------------
document.addEventListener('DOMContentLoaded', () => {
  // Populate Doctor Select
  const docSelect = document.getElementById('doctorSelect');
  doctors.forEach((doc, idx) => {
    const opt = document.createElement('option');
    opt.value = idx;
    opt.textContent = `${doc.name} (${doc.specialization}) - $${doc.consultationFee}`;
    docSelect.appendChild(opt);
  });

  // Triage Evaluation Trigger
  document.getElementById('btnEvaluateTriage').addEventListener('click', () => {
    const symptoms = document.getElementById('symptomInput').value;
    const bp = parseInt(document.getElementById('bpInput').value, 10);

    if (!symptoms) {
      alert('Please enter patient reported symptoms.');
      return;
    }

    const res = triageEngine.evaluate(symptoms, bp);
    const box = document.getElementById('triageResultBox');
    box.className = `status-banner status-${res.acuity.toLowerCase()}`;
    box.innerHTML = `
      <strong>Triage Assessment Result:</strong><br>
      • Acuity Level: <strong>${res.acuity}</strong> (Priority Score: ${res.urgencyScore}/100)<br>
      • Recommended Department: <strong>${res.specialty}</strong><br>
      • Assessed At: ${res.evaluatedAt}
    `;

    // Auto-select best matching doctor if available
    doctors.forEach((d, idx) => {
      if (d.specialization.toLowerCase() === res.specialty.toLowerCase()) {
        docSelect.selectedIndex = idx;
      }
    });

    window.lastTriageAcuity = res.acuity;
    updateInspector();
  });

  // Book Appointment Form
  document.getElementById('appointmentForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const docIdx = docSelect.value;
    const selectedDoctor = doctors[docIdx];
    const slot = document.getElementById('apptDateTime').value;

    if (!slot) {
      alert('Please select an appointment time slot.');
      return;
    }

    const apptId = `APT-${Math.floor(1000 + Math.random() * 9000)}`;
    const acuity = window.lastTriageAcuity || 'ROUTINE';
    const appt = new Appointment(apptId, currentPatient, selectedDoctor, slot, acuity);
    appointments.push(appt);

    renderAppointments();
    updateInspector();
    alert(`Appointment ${apptId} successfully booked with ${selectedDoctor.name}!`);
  });

  // Doctor Consultation & Prescription Generation
  document.getElementById('consultationForm').addEventListener('submit', (e) => {
    e.preventDefault();
    if (appointments.length === 0) {
      alert('Please schedule an appointment first before conducting consultation.');
      return;
    }

    const latestAppt = appointments[appointments.length - 1];
    latestAppt.complete();

    const diagnosis = document.getElementById('diagnosisInput').value;
    const vitalsStr = document.getElementById('vitalsInput').value;
    const treatment = document.getElementById('treatmentInput').value;
    const medsInput = document.getElementById('medsInput').value;

    // Create MedicalRecord (Class 4)
    const recId = `MR-${Math.floor(1000 + Math.random() * 9000)}`;
    const newRecord = new MedicalRecord(
      recId,
      latestAppt.patient.userId,
      latestAppt.doctor.userId,
      diagnosis,
      vitalsStr,
      treatment
    );
    records.push(newRecord);
    currentPatient.records.push(newRecord);

    // Create Prescription (Class 5)
    const rxId = `RX-${Math.floor(1000 + Math.random() * 9000)}`;
    const newRx = new Prescription(
      rxId,
      latestAppt.appointmentId,
      latestAppt.patient.name,
      latestAppt.doctor.name,
      medsInput.split('\n').filter(Boolean),
      treatment
    );
    prescriptions.push(newRx);
    currentPatient.prescriptions.push(newRx);

    renderAppointments();
    renderRecordsAndPrescriptions();
    updateInspector();
    alert(`Consultation complete. Record ${recId} and Prescription ${rxId} generated!`);
  });

  renderAppointments();
  updateInspector();
});

function renderAppointments() {
  const container = document.getElementById('appointmentsList');
  if (appointments.length === 0) {
    container.innerHTML = '<p style="color:#64748b; font-size:0.9rem;">No active appointments scheduled yet.</p>';
    return;
  }

  container.innerHTML = appointments.map(appt => `
    <div class="item-card">
      <div class="item-header">
        <span>${appt.appointmentId} - ${appt.doctor.name}</span>
        <span class="badge badge-${appt.status.toLowerCase()}">${appt.status}</span>
      </div>
      <div><strong>Specialty:</strong> ${appt.doctor.specialization}</div>
      <div><strong>Slot:</strong> ${appt.dateTime.replace('T', ' ')}</div>
      <div><strong>Priority:</strong> <span class="badge badge-${appt.triagePriority.toLowerCase()}">${appt.triagePriority}</span></div>
    </div>
  `).join('');
}

function renderRecordsAndPrescriptions() {
  const recContainer = document.getElementById('recordsList');
  if (records.length === 0) {
    recContainer.innerHTML = '<p style="color:#64748b; font-size:0.9rem;">No EHR records available yet.</p>';
    return;
  }

  recContainer.innerHTML = records.map((r, i) => {
    const rx = prescriptions[i];
    return `
      <div class="item-card" style="border-left: 4px solid #1e40af;">
        <div class="item-header">
          <span>${r.recordId} (Diagnosis: ${r.diagnosis})</span>
          <span style="font-size:0.8rem; color:#64748b;">${r.timestamp}</span>
        </div>
        <div><strong>Vitals:</strong> ${r.vitals}</div>
        <div><strong>Treatment:</strong> ${r.treatmentPlan}</div>
        ${rx ? `
          <div style="margin-top:8px; padding-top:8px; border-top:1px dashed #cbd5e1;">
            <strong>Prescription (${rx.prescriptionId}):</strong>
            <ul style="margin-left: 20px; font-size: 0.85rem;">
              ${rx.medications.map(m => `<li>${m}</li>`).join('')}
            </ul>
          </div>
        ` : ''}
      </div>
    `;
  }).join('');
}

function updateInspector() {
  const inspector = document.getElementById('runtimeObjectsDisplay');
  const snapshot = {
    "Active_Classes_Instantiated": [
      "User (Abstract Base)",
      "Patient (subclass of User)",
      "Doctor (subclass of User)",
      "Appointment",
      "MedicalRecord",
      "Prescription",
      "TriageEngine"
    ],
    "Current_Patient_Instance": currentPatient,
    "Selected_Doctor_Instances_Count": doctors.length,
    "Appointments_Created": appointments,
    "Electronic_Health_Records": records,
    "Prescriptions_Issued": prescriptions
  };
  inspector.textContent = JSON.stringify(snapshot, null, 2);
}