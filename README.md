# ระบบลงทะเบียนเรียนล่วงหน้า (Student Registration System)

## คำอธิบายโครงการ

โปรแกรมระบบลงทะเบียนเรียนล่วงหน้าสำหรับนักเรียนระดับมัธยมปลายที่ต้องการเรียนวิชาระดับปริญญาตรีปีที่ 1 ล่วงหน้า พัฒนาด้วยแนวคิด MVC (Model-View-Controller) Design Pattern

## โครงสร้างโปรแกรม (MVC Architecture)

### Model

- **`models/database_manager.py`** - จัดการฐานข้อมูล SQLite และ Business Logic หลัก
  - การสร้างและจัดการตาราง
  - การตรวจสอบข้อมูล (Validation)
  - การดำเนินการ CRUD (Create, Read, Update, Delete)
  - การตรวจสอบวิชาบังคับก่อน
  - การคำนวณ GPA และหน่วยกิต

### View

- **`views/login_view.py`** - หน้าจอเข้าสู่ระบบ
- **`views/student_view.py`** - หน้าจอสำหรับนักเรียน (ประวัติ + ลงทะเบียน)
- **`views/admin_view.py`** - หน้าจอสำหรับแอดมิน (จัดการนักเรียน + กรอกเกรด)

### Controller

- **`controllers/auth_controller.py`** - จัดการการยืนยันตัวตน
- **`controllers/student_controller.py`** - จัดการฟังก์ชันของนักเรียน
- **`controllers/admin_controller.py`** - จัดการฟังก์ชันของแอดมิน

### Main Application

- **`main.py`** - ไฟล์หลักที่เชื่อมโยงทุกส่วนเข้าด้วยกัน

## ฐานข้อมูล

### ตาราง (Tables)

1. **Students** - ข้อมูลนักเรียน

   - student_id (PK) - รหัสนักเรียน 8 หลัก (69xxxxxx)
   - prefix, first_name, last_name - คำนำหน้า, ชื่อ, นามสกุล
   - birth_date - วันเกิด
   - current_school - โรงเรียนปัจจุบัน
   - email - อีเมล
   - program_code - รหัสหลักสูตร
   - password - รหัสผ่าน

2. **Programs** - หลักสูตร

   - program_code (PK) - รหัสหลักสูตร 8 หลัก
   - program_name - ชื่อหลักสูตร
   - department - ชื่อภาควิชา

3. **Subjects** - รายวิชา

   - subject_code (PK) - รหัสวิชา 8 หลัก (05500xxx สำหรับวิชาคณะ, 90690xxx สำหรับวิชาศึกษาทั่วไป)
   - subject_name - ชื่อวิชา
   - credits - หน่วยกิต
   - instructor - อาจารย์ผู้สอน
   - prerequisite - รหัสวิชาบังคับก่อน

4. **SubjectStructure** - โครงสร้างหลักสูตร

   - program_code, subject_code - ความสัมพันธ์ระหว่างหลักสูตรและวิชา
   - semester - เทอมที่เปิดสอน (1 หรือ 2)

5. **RegisteredSubject** - การลงทะเบียนและเกรด

   - student_id, subject_code - นักเรียนที่ลงทะเบียนในวิชา
   - grade - เกรดที่ได้รับ (A, B+, B, C+, C, D+, D, F, IP)
   - registration_date - วันที่ลงทะเบียน

6. **Admin** - ผู้ดูแลระบบ
   - admin_id (PK) - รหัสแอดมิน
   - username - ชื่อผู้ใช้
   - password - รหัสผ่าน

## คุณสมบัติหลัก (Features)

### สำหรับนักเรียน

- เข้าสู่ระบบด้วยรหัสนักเรียน
- ดูประวัติส่วนตัว, GPA, และหน่วยกิตที่ผ่าน
- ดูรายวิชาที่ลงทะเบียนแล้วและเกรด
- ลงทะเบียนวิชาใหม่ (ตรวจสอบวิชาบังคับก่อนอัตโนมัติ)
- ตรวจสอบอายุขั้นต่ำ 15 ปี

### สำหรับแอดมิน

- เข้าสู่ระบบด้วยบัญชีแอดมิน
- ดูรายชื่อนักเรียนทั้งหมด
- ค้นหา กรอง และเรียงลำดับนักเรียน
- ดูประวัติของนักเรียนแต่ละคน
- กรอกเกรดสำหรับรายวิชาต่างๆ
- ดูสถิติการลงทะเบียน

### Business Rules

- นักเรียนต้องมีอายุอย่างน้อย 15 ปี
- ต้องผ่านวิชาบังคับก่อน (เกรดไม่เป็น F หรือ IP)
- ไม่สามารถลงทะเบียนวิชาซ้ำได้
- เมื่อลงทะเบียนสำเร็จจะกลับไปหน้าประวัติ

## การติดตั้งและรันโปรแกรม

### ความต้องการของระบบ

- Python 3.7+
- โมดูลที่ใช้ทั้งหมดเป็น Standard Library ของ Python

### วิธีการรัน

```bash
python main.py
```

### ข้อมูลสำหรับทดสอบ

#### บัญชีแอดมิน

- Username: `admin`
- Password: `admin123`

#### บัญชีนักเรียน (ตัวอย่าง)

- รหัสนักเรียน: `69000001`
- รหัสผ่าน: `password123`

(มีนักเรียนตัวอย่าง 11 คน รหัส 69000001-69000011)

### โครงสร้างไฟล์

```
student_registration_system/
│
├── main.py                          # ไฟล์หลัก
├── models/
│   └── database_manager.py          # Model - จัดการฐานข้อมูล
├── views/
│   ├── login_view.py                # View - หน้าเข้าสู่ระบบ
│   ├── student_view.py              # View - หน้านักเรียน
│   └── admin_view.py                # View - หน้าแอดมิน
├── controllers/
│   ├── auth_controller.py           # Controller - ยืนยันตัวตน
│   ├── student_controller.py        # Controller - ฟังก์ชันนักเรียน
│   └── admin_controller.py          # Controller - ฟังก์ชันแอดมิน
├── requirements.txt                 # Dependencies (ไม่มี external libs)
├── README.md                        # เอกสารอธิบาย
└── student_registration.db          # ฐานข้อมูล SQLite (สร้างอัตโนมัติ)
```

## ข้อมูลตัวอย่างที่เตรียมไว้

### หลักสูตร (3 หลักสูตร)

1. วิทยาการคอมพิวเตอร์
2. วิศวกรรมซอฟต์แวร์
3. คณิตศาสตร์ประยุกต์

### รายวิชา (11 วิชา)

- วิชาคณะ: Computer Programming I/II, Data Structures, Database Systems, etc.
- วิชาศึกษาทั่วไป: English I/II, Mathematics I/II

### นักเรียน (11 คน)

- รหัสนักเรียนเริ่มด้วย 69 ตามข้อกำหนด
- มีข้อมูลครบถ้วนตามโครงสร้างตาราง

## การใช้งาน

1. รันโปรแกรมด้วย `python main.py`
2. เข้าสู่ระบบด้วยบัญชีนักเรียนหรือแอดมิน
3. ใช้ฟีเจอร์ต่างๆ ตามสิทธิ์การเข้าถึง
4. ออกจากระบบเมื่อเสร็จสิ้นการใช้งาน

## หมายเหตุ

- โปรแกรมใช้ SQLite เป็นฐานข้อมูล (ไฟล์ student_registration.db)
- ข้อมูลตัวอย่างจะถูกสร้างอัตโนมัติในการรันครั้งแรก
- GUI ใช้ Tkinter ซึ่งเป็น Standard Library ของ Python
- ระบบปฏิบัติตาม SOLID Principles และ MVC Pattern
- ไม่มีการจัดการ Security เชิงลึกตามข้อกำหนดของโจทย์
