class Student:
    def __init__(self, student_id, name, age, grade):
        # Attributes
        self.student_id = student_id      
        self.name = name                  
        self.age = age                    
        self.grade = grade               
        self.subjects = []                

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
            return "มัธยมปลาย"
        elif 19 <= self.age < 22:
            return "อุดมศึกษา"
        else:
            return "บุคคลทั่วไป"

    def display_info(self):
        print("=== ข้อมูลนักเรียน ===")
        print(f"รหัสนักเรียน : {self.student_id}")
        print(f"ชื่อ : {self.name}")
        print(f"อายุ : {self.age} ปี")
        print(f"เกรดเฉลี่ย : {self.grade}")
        print(f"ระดับชั้น : {self.calculate_grade_level()}")
        print(f"รายวิชาที่เรียน : {', '.join(self.subjects) if self.subjects else 'ยังไม่มีรายวิชา'}")
        print("======================")

    def __str__(self):
        return f"{self.student_id} - {self.name} ({self.age} ปี, GPA: {self.grade})"

if __name__ == "__main__":
    s1 = Student("ST001", "สมชาย ใจดี", 20, 3.00)
    s1.add_subject("คณิตศาสตร์")
    s1.add_subject("วิทยาศาสตร์")
    s1.add_subject("ภาษาอังกฤษ")
    s1.remove_subject("ภาษาอังกฤษ")
    s1.display_info()

    print(s1)