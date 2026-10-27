# MediPulse AI: Intelligent Clinical Workflow Automation & Telehealth Ecosystem
### Final Capstone Project Proposal & Prototyping (Part I)
**Student Name:** Khalid Mansoor  
**Course:** CSE-499: Senior Capstone Project  
**Submission Requirement:** GitHub Repository Link with Full Proposal, UML Diagrams, Gantt Chart & 5+ Class Prototype  
**Evaluation Points:** 30 / 30 Points  

---

## 🌟 Executive Overview
**MediPulse AI** is an intelligent, scalable, object-oriented clinical management and automated triage platform. It streamlines the patient intake lifecycle: from AI-assisted symptom triage and priority score allocation, through physician tele-consultation and electronic health record (EHR) documentation, to digital prescription dispatch.

---

## 📁 Repository Directory Structure

```text
medipulse-ai-capstone/
│
├── proposal.tex             # Master LaTeX Document (Self-contained, with native TikZ diagrams & Gantt chart)
├── references.bib           # BibTeX citations and academic bibliography
├── proposal.html            # Standalone visual document (Open in browser & Print to PDF with 1-click)
├── CHAT_AND_PROJECT_GUIDE.html # Complete chat transcript & visual project documentation
├── CHAT_AND_PROJECT_GUIDE.md   # Markdown project walkthrough
├── README.md                # Project documentation, architecture, and submission guide
│
└── prototype/               # Interactive Prototype Implementation (Exercising 6 UML Classes)
    ├── models.py            # Python OOP implementation (User, Patient, Doctor, Appointment, MedicalRecord, Prescription)
    ├── main.py              # Interactive console demonstration script
    ├── index.html           # Modern interactive web interface dashboard
    ├── styles.css           # Healthcare-styled responsive stylesheet
    └── app.js               # Frontend JavaScript domain classes & Live Object Inspector
```

---

## 🎯 Verification of All Assignment Requirements

| Requirement | Description in Project | Implementation Location |
| :--- | :--- | :--- |
| **Project Idea** | MediPulse AI: Clinical Workflow Automation & Telehealth Triage | `proposal.tex`, `proposal.html` (Sec 1) |
| **Professional Proposal** | Problem Statement, Scope, Feasibility (Technical, Operational, Economic, Legal/HIPAA) | `proposal.tex`, `proposal.html` (Sec 1-2) |
| **Software Process Model** | Agile Scrum with 6 two-week sprint cadences and milestone matrix | `proposal.tex`, `proposal.html` (Sec 3) |
| **Schedules & Milestones** | 14-week WBS, milestone gates (M1 to M5), and deliverables | `proposal.tex`, `proposal.html` (Table 3.1) |
| **Gantt Chart** | Visual project timeline mapped from Week 1 to 14 | `proposal.tex` (pgfgantt), `proposal.html` |
| **DFD Diagram** | Level 0 Context Diagram + Level 1 Process Decomposition | `proposal.tex`, `proposal.html` (Sec 4.1) |
| **Use Case Diagram** | Actors (Patient, Doctor, Admin), include/extend relations | `proposal.tex`, `proposal.html` (Sec 4.2) |
| **Activity Diagram** | Workflow swimlanes, severity branching, consultation flow | `proposal.tex`, `proposal.html` (Sec 4.3) |
| **ER Diagram (ERD)** | Relational entities, Primary Keys, Foreign Keys, Cardinalities | `proposal.tex`, `proposal.html` (Sec 4.4) |
| **Class Diagram** | 6 classes, inheritance, visibility (+, -, #), typed signatures | `proposal.tex`, `proposal.html` (Sec 4.5) |
| **Object Diagram** | Runtime snapshot instances, concrete values, object links | `proposal.tex`, `proposal.html` (Sec 4.6) |
| **5+ Classes Interface** | Prototype interface exercising 6 interconnected domain classes | `prototype/` (Web + Python CLI) |
| **LaTeX Code & PDF** | Full LaTeX source code + instant PDF generation method | `proposal.tex`, `proposal.html` |

---

## 🧩 The 6 UML Classes Implemented in the Prototype

1. **`User`** (Abstract Base Class): Encapsulates `user_id`, `name`, `email`, `phone`, `role`, and abstract method `get_dashboard_summary()`.
2. **`Patient`** (Subclass of `User`): Implements `dob`, `blood_group`, `insurance_id`, maintains collections of `MedicalRecord` and `Prescription` instances.
3. **`Doctor`** (Subclass of `User`): Implements `specialization`, `license_number`, `consultation_fee`, conducts consultations, and signs prescriptions.
4. **`Appointment`**: Associates `Patient` and `Doctor`, tracking `appointment_id`, `date_time`, `triage_priority` (CRITICAL, URGENT, ROUTINE), and `status`.
5. **`MedicalRecord`**: Encapsulates clinical `diagnosis`, physiological `vitals` (BP, HR, SpO2, Temp), and `treatment_plan`.
6. **`Prescription`**: Encapsulates medication orders (drug name, dosage, frequency, duration), administration guidelines, and fulfillment status.
7. **`TriageEngine`** *(Bonus Class)*: Evaluates symptom text and vital signs to assign acuity ratings and automatically recommend medical specialties.

---

## 🚀 How to Run the Prototype

### Option 1: Interactive Web Dashboard (Recommended)
1. Navigate to the `prototype/` folder.
2. Double-click `index.html` to open it in any web browser (Chrome, Edge, Firefox, Safari).
3. **What you can do in the interface:**
   - Submit symptoms and test the **AI Triage Engine**.
   - Watch the triage acuity classification change to **CRITICAL** or **ROUTINE**.
   - Schedule an **Appointment** with the recommended specialist.
   - Enter clinical diagnosis, vitals, and generate an **EHR Medical Record**.
   - Issue and format a **Digital Prescription**.
   - Inspect the **Live Runtime Object Inspector** at the bottom, which visualizes the live memory state of all instantiated classes!

### Option 2: Python Terminal Execution
Open your terminal in `medipulse-ai-capstone` and run:
```bash
python prototype/main.py
```
This executes an end-to-end clinical workflow script that instantiates all 6 classes, validates data integrity, and logs detailed execution traces.

---

## 📄 How to Compile the LaTeX Proposal to PDF

### Method A: Overleaf (1-Click, Recommended for Submission)
1. Go to [Overleaf](https://www.overleaf.com).
2. Create a **New Project** -> **Upload Project**.
3. Upload `proposal.tex` and `references.bib`.
4. Click **Recompile**.
5. Download your publication-ready PDF!

### Method B: Local LaTeX Installation (pdflatex / TeX Live / MiKTeX)
Run the following in the project directory:
```bash
pdflatex proposal.tex
bibtex proposal
pdflatex proposal.tex
pdflatex proposal.tex
```

### Method C: Instant PDF from HTML
1. Open `proposal.html` in Google Chrome or Microsoft Edge.
2. Press `Ctrl + P` (or Cmd + P on macOS).
3. Set Destination to **"Save as PDF"**.
4. Check **"Background graphics"**.
5. Click **Save**. You will get a print-ready A4 PDF with all embedded SVG diagrams!
