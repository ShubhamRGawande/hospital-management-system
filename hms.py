import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import sys
import re

# Constants
DATA_FILE = "hospital_data.json"
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M"


class MenuOption(Enum):
    MANAGE_PATIENTS = 1
    MANAGE_DOCTORS = 2
    APPOINTMENTS = 3
    INPATIENT_MGMT = 4
    BILLING = 5
    REPORTS = 6
    EXIT = 7


@dataclass
class Address:
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "USA"


@dataclass
class MedicalRecord:
    record_id: str
    patient_id: str
    diagnosis: str
    treatment: str
    date: str
    doctor_id: str
    notes: str = ""


@dataclass
class Appointment:
    appointment_id: str
    patient_id: str
    doctor_id: str
    date: str
    time: str
    reason: str
    status: str = "Scheduled"  # Scheduled, Completed, Cancelled


@dataclass
class BillingRecord:
    bill_id: str
    patient_id: str
    amount: float
    date_issued: str
    date_paid: Optional[str] = None
    services: List[str] = None

    def __post_init__(self):
        if self.services is None:
            self.services = []


@dataclass
class Person:
    first_name: str
    last_name: str
    date_of_birth: str
    gender: str
    address: Address
    phone: str
    email: str


@dataclass
class Patient(Person):
    patient_id: str
    blood_type: Optional[str] = None
    allergies: List[str] = None
    medical_records: List[MedicalRecord] = None
    appointments: List[Appointment] = None
    bills: List[BillingRecord] = None

    def __post_init__(self):
        if self.allergies is None:
            self.allergies = []
        if self.medical_records is None:
            self.medical_records = []
        if self.appointments is None:
            self.appointments = []
        if self.bills is None:
            self.bills = []


@dataclass
class Doctor(Person):
    doctor_id: str
    specialization: str
    license_number: str
    schedule: Dict[str, List[str]] = None  # Day: [available times]

    def __post_init__(self):
        if self.schedule is None:
            self.schedule = {
                "Monday": ["09:00", "11:00", "14:00"],
                "Tuesday": ["10:00", "13:00", "15:00"],
                # ... other days
            }


class HospitalManagementSystem:
    def __init__(self):
        self.patients: Dict[str, Patient] = {}
        self.doctors: Dict[str, Doctor] = {}
        self.appointments: Dict[str, Appointment] = {}
        self.load_data()

    def load_data(self):
        """Load hospital data from JSON file"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as file:
                    data = json.load(file)
                    # Load patients
                    for patient_id, patient_data in data.get('patients', {}).items():
                        address_data = patient_data.pop('address')
                        address = Address(**address_data)

                        medical_records = [
                            MedicalRecord(**record) for record in patient_data.get('medical_records', [])
                        ]

                        appointments = [
                            Appointment(**appt) for appt in patient_data.get('appointments', [])
                        ]

                        bills = [
                            BillingRecord(**bill) for bill in patient_data.get('bills', [])
                        ]

                        self.patients[patient_id] = Patient(
                            address=address,
                            medical_records=medical_records,
                            appointments=appointments,
                            bills=bills,
                            **patient_data
                        )

                    # Load doctors
                    for doctor_id, doctor_data in data.get('doctors', {}).items():
                        address_data = doctor_data.pop('address')
                        address = Address(**address_data)
                        self.doctors[doctor_id] = Doctor(
                            address=address,
                            **doctor_data
                        )

                    # Load appointments
                    for appt_id, appt_data in data.get('appointments', {}).items():
                        self.appointments[appt_id] = Appointment(**appt_data)

            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading data: {e}. Starting with empty database.")

    def save_data(self):
        """Save hospital data to JSON file"""
        data = {
            'patients': {p.patient_id: asdict(p) for p in self.patients.values()},
            'doctors': {d.doctor_id: asdict(d) for d in self.doctors.values()},
            'appointments': {a.appointment_id: asdict(a) for a in self.appointments.values()}
        }
        with open(DATA_FILE, 'w') as file:
            json.dump(data, file, indent=2)

    # Helper methods
    def generate_id(self, prefix: str = "ID") -> str:
        """Generate a unique ID with given prefix"""
        existing_ids = [
            int(id[len(prefix):]) for id in self.patients.keys()
            if id.startswith(prefix) and id[len(prefix):].isdigit()
        ]
        new_id = max(existing_ids) + 1 if existing_ids else 1
        return f"{prefix}{new_id:04d}"

    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def validate_phone(self, phone: str) -> bool:
        """Validate phone number format"""
        pattern = r'^\+?[\d\s-]{10,}$'
        return re.match(pattern, phone) is not None

    def validate_date(self, date_str: str) -> bool:
        """Validate date format (YYYY-MM-DD)"""
        try:
            datetime.strptime(date_str, DATE_FORMAT)
            return True
        except ValueError:
            return False

    def validate_time(self, time_str: str) -> bool:
        """Validate time format (HH:MM)"""
        try:
            datetime.strptime(time_str, TIME_FORMAT)
            return True
        except ValueError:
            return False

    def _press_enter_to_continue(self):
        """Utility method to pause execution"""
        input("\nPress Enter to continue...")

    # Patient Management
    def add_patient(self):
        """Add a new patient to the system"""
        print("\n" + "=" * 50)
        print("ADD NEW PATIENT".center(50))
        print("=" * 50)

        # Get basic info
        first_name = input("First Name: ").strip()
        last_name = input("Last Name: ").strip()

        while True:
            email = input("Email: ").strip()
            if self.validate_email(email):
                break
            print("Invalid email format. Please try again.")

        while True:
            phone = input("Phone: ").strip()
            if self.validate_phone(phone):
                break
            print("Invalid phone number. Please try again.")

        while True:
            dob = input("Date of Birth (YYYY-MM-DD): ").strip()
            if self.validate_date(dob):
                break
            print("Invalid date format. Please use YYYY-MM-DD.")

        gender = input("Gender (M/F/O): ").strip().upper()
        blood_type = input("Blood Type (optional): ").strip().upper()

        # Get address
        print("\nAddress Information:")
        street = input("Street: ").strip()
        city = input("City: ").strip()
        state = input("State: ").strip()
        zip_code = input("ZIP Code: ").strip()

        address = Address(
            street=street,
            city=city,
            state=state,
            zip_code=zip_code
        )

        # Create patient
        patient_id = self.generate_id("PAT")
        new_patient = Patient(
            patient_id=patient_id,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=dob,
            gender=gender,
            address=address,
            phone=phone,
            email=email,
            blood_type=blood_type if blood_type else None
        )

        self.patients[patient_id] = new_patient
        self.save_data()

        print(f"\nPatient added successfully! Patient ID: {patient_id}")
        self._press_enter_to_continue()

    def view_patients(self, patients: Optional[List[Patient]] = None):
        """Display a list of patients"""
        patients_to_display = patients if patients is not None else list(self.patients.values())

        print("\n" + "=" * 100)
        print("PATIENT RECORDS".center(100))
        print("=" * 100)
        print(f"{'ID':<8}{'Name':<25}{'Gender':<8}{'DOB':<12}{'Phone':<15}{'Email':<30}")
        print("-" * 100)

        for patient in patients_to_display:
            name = f"{patient.first_name} {patient.last_name}"
            print(f"{patient.patient_id:<8}{name:<25}{patient.gender:<8}"
                  f"{patient.date_of_birth:<12}{patient.phone:<15}{patient.email:<30}")

        print("=" * 100)
        self._press_enter_to_continue()

    # Doctor Management
    def add_doctor(self):
        """Add a new doctor to the system"""
        print("\n" + "=" * 50)
        print("ADD NEW DOCTOR".center(50))
        print("=" * 50)

        # Get basic info
        first_name = input("First Name: ").strip()
        last_name = input("Last Name: ").strip()
        specialization = input("Specialization: ").strip()
        license_number = input("License Number: ").strip()

        while True:
            email = input("Email: ").strip()
            if self.validate_email(email):
                break
            print("Invalid email format. Please try again.")

        while True:
            phone = input("Phone: ").strip()
            if self.validate_phone(phone):
                break
            print("Invalid phone number. Please try again.")

        # Get address
        print("\nAddress Information:")
        street = input("Street: ").strip()
        city = input("City: ").strip()
        state = input("State: ").strip()
        zip_code = input("ZIP Code: ").strip()

        address = Address(
            street=street,
            city=city,
            state=state,
            zip_code=zip_code
        )

        # Create doctor
        doctor_id = self.generate_id("DOC")
        new_doctor = Doctor(
            doctor_id=doctor_id,
            first_name=first_name,
            last_name=last_name,
            specialization=specialization,
            license_number=license_number,
            address=address,
            phone=phone,
            email=email,
            gender=input("Gender (M/F/O): ").strip().upper(),
            date_of_birth=input("Date of Birth (YYYY-MM-DD): ").strip()
        )

        self.doctors[doctor_id] = new_doctor
        self.save_data()

        print(f"\nDoctor added successfully! Doctor ID: {doctor_id}")
        self._press_enter_to_continue()

    # Appointment Management
    def schedule_appointment(self):
        """Schedule a new appointment"""
        print("\n" + "=" * 50)
        print("SCHEDULE APPOINTMENT".center(50))
        print("=" * 50)

        # Select patient
        patient_id = input("Enter Patient ID: ").strip()
        if patient_id not in self.patients:
            print("Patient not found!")
            self._press_enter_to_continue()
            return

        # Select doctor
        print("\nAvailable Doctors:")
        for doctor_id, doctor in self.doctors.items():
            print(f"{doctor_id}: Dr. {doctor.last_name} ({doctor.specialization})")

        doctor_id = input("\nEnter Doctor ID: ").strip()
        if doctor_id not in self.doctors:
            print("Doctor not found!")
            self._press_enter_to_continue()
            return

        # Get appointment details
        while True:
            date = input("Date (YYYY-MM-DD): ").strip()
            if self.validate_date(date):
                break
            print("Invalid date format. Please use YYYY-MM-DD.")

        while True:
            time = input("Time (HH:MM): ").strip()
            if self.validate_time(time):
                break
            print("Invalid time format. Please use HH:MM.")

        reason = input("Reason for appointment: ").strip()

        # Create appointment
        appointment_id = self.generate_id("APT")
        new_appointment = Appointment(
            appointment_id=appointment_id,
            patient_id=patient_id,
            doctor_id=doctor_id,
            date=date,
            time=time,
            reason=reason
        )

        # Add to both systems
        self.appointments[appointment_id] = new_appointment
        self.patients[patient_id].appointments.append(new_appointment)
        self.save_data()

        print(f"\nAppointment scheduled successfully! Appointment ID: {appointment_id}")
        self._press_enter_to_continue()

    # Main menu and execution
    def display_main_menu(self):
        """Display the main menu"""
        print("\n" + "=" * 50)
        print("HOSPITAL MANAGEMENT SYSTEM".center(50))
        print("=" * 50)
        print(f"{MenuOption.MANAGE_PATIENTS.value}. Patient Management")
        print(f"{MenuOption.MANAGE_DOCTORS.value}. Doctor Management")
        print(f"{MenuOption.APPOINTMENTS.value}. Appointment Management")
        print(f"{MenuOption.INPATIENT_MGMT.value}. Inpatient Management")
        print(f"{MenuOption.BILLING.value}. Billing")
        print(f"{MenuOption.REPORTS.value}. Reports")
        print(f"{MenuOption.EXIT.value}. Exit")
        print("=" * 50)

    def run(self):
        """Main application loop"""
        while True:
            self.display_main_menu()

            try:
                choice = int(input("Enter your choice (1-7): "))
                menu_option = MenuOption(choice)

                if menu_option == MenuOption.MANAGE_PATIENTS:
                    self.manage_patients()
                elif menu_option == MenuOption.MANAGE_DOCTORS:
                    self.manage_doctors()
                elif menu_option == MenuOption.APPOINTMENTS:
                    self.manage_appointments()
                elif menu_option == MenuOption.INPATIENT_MGMT:
                    print("Inpatient management module coming soon!")
                    self._press_enter_to_continue()
                elif menu_option == MenuOption.BILLING:
                    print("Billing module coming soon!")
                    self._press_enter_to_continue()
                elif menu_option == MenuOption.REPORTS:
                    print("Reports module coming soon!")
                    self._press_enter_to_continue()
                elif menu_option == MenuOption.EXIT:
                    print("Exiting Hospital Management System. Goodbye!")
                    break

            except ValueError:
                print("Invalid input. Please enter a number between 1 and 7.")
                self._press_enter_to_continue()


def main():
    """Entry point for the application"""
    system = HospitalManagementSystem()
    try:
        system.run()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Saving data...")
        system.save_data()
        sys.exit(0)


if __name__ == "__main__":
    main()