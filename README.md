 🏥 Hospital Management System (Python CLI)

A comprehensive **Hospital Management System** built with Python using Object-Oriented Programming, Data Classes, JSON-based data persistence, and a Command-Line Interface (CLI). This system helps manage patients, doctors, appointments, billing, and medical records in a structured and user-friendly way.



 📌 Features

- 🔹 Add/View Patients
- 🔹 Add/View Doctors
- 🔹 Schedule and Manage Appointments
- 🔹 Generate and Track Billing Records
- 🔹 Store Medical Records
- 🔹 Save & Load Data with JSON
- 🔹 Input validation for dates, emails, phone numbers, etc.

 🧰 Tech Stack

- **Language:** Python 3.x
- **Libraries:** `json`, `datetime`, `dataclasses`, `enum`, `typing`, `re`, `os`, `sys`
- **Data Storage:** JSON (`hospital_data.json`)


 🚀 How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/hospital-management-system.git
   cd hospital-management-system
   ```

2. **Make sure you have Python 3 installed**
   ```bash
   python3 --version
   ```

3. **Run the main file**
   ```bash
   python3 main.py
   ```

> ⚠️ Note: Replace `main.py` with the actual filename that contains the `HospitalManagementSystem` runner or menu logic.

---

### 📂 File Structure

```
hospital-management-system/
│
├── hospital_data.json        # JSON file to persist hospital data
├── main.py                   # Main Python file (CLI logic)
├── README.md                 # Project documentation
```

---

### 📈 Future Improvements

- Add GUI using Tkinter or PyQt
- Integrate database (SQLite/MySQL)
- Role-based access control (Admin, Doctor, Receptionist)
- Export reports (PDF/CSV)

---

### 🤝 Contributing

Feel free to fork this repository and submit a pull request with improvements. Contributions are welcome!

---

### 🪪 License

This project is open-source and available under the [MIT License](LICENSE).
