class CollegeStudent:
    def __init__(self, student_id, name, age, grade, major, gpa):
        self.student_id = student_id      
        self.name = name                
        self.age = age                   
        self.grade = grade                
        self.subjects = []                

        self.major = major                
        self.credits = 0                  
        self.gpa = gpa                    

    def add_subject(self, subject_name):
        if subject_name not in self.subjects:
            self.subjects.append(subject_name)

    def remove_subject(self, subject_name):
        if subject_name in self.subjects:
            self.subjects.remove(subject_name)

    def calculate_grade_level(self):
        if self.age < 13:
            return "ประถมศึกษา"
        elif 13 <= self.age < 16:
            return "มัธยมต้น"
        elif 16 <= self.age < 19:
            return "มัธยมปลาย / ปวช."
        elif 19 <= self.age < 22:
            return "อุดมศึกษา / ปวส."
        else:
            return "บุคคลทั่วไป / ศึกษาต่อ"

    def add_credits(self, credit_amount):
        if credit_amount > 0:
            self.credits += credit_amount

    def calculate_tuition(self):
        return self.credits * 1500
    
    def update_gpa(self, new_gpa):
        if 0.0 <= new_gpa <= 4.0:
            self.gpa = new_gpa
        else:
            print("ค่า GPA ต้องอยู่ระหว่าง 0.00 - 4.00")

    def get_academic_status(self):
        return "ปกติ" if self.gpa >= 2.0 else "พักการเรียน"

    def display_info(self):
        print("=== ข้อมูลนักเรียน ===")
        print(f"รหัสนักเรียน : {self.student_id}")
        print(f"ชื่อ : {self.name}")
        print(f"อายุ : {self.age} ปี")
        print(f"เกรดเฉลี่ย : {self.grade}")
        print(f"ระดับชั้น : {self.calculate_grade_level()}")
        print(f"รายวิชาที่เรียน : {', '.join(self.subjects) if self.subjects else 'ยังไม่มีรายวิชา'}")
        print("======================")
        print(f"สาขาวิชา : {self.major}")
        print(f"หน่วยกิตที่ลงทะเบียน : {self.credits}")
        print(f"GPA สะสม : {self.gpa}")
        print(f"สถานะการเรียน : {self.get_academic_status()}")
        print(f"ค่าเทอม : {self.calculate_tuition():,.0f} บาท")
        print("======================")

    def __str__(self):
        return (f"{self.student_id} - {self.name} ({self.age} ปี, GPA: {self.gpa})\n"
                f"สาขา: {self.major}, หน่วยกิต: {self.credits}, สถานะ: {self.get_academic_status()}")

if __name__ == "__main__":
    student = CollegeStudent("ST001", "สมชาย ใจดี", 18, 4.0, "เทคโนโลยีสารสนเทศ", 3.00)
    student.add_subject("คณิตศาสตร์")
    student.add_subject("วิทยาศาสตร์")
    student.add_credits(15)         
    student.update_gpa(1.00)        

  
    student.display_info()

  
    print(student)