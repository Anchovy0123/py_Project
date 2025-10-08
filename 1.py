class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
    
    def print_info(self):
        print(f"ชื่อ: {self.name}, เกรด: {self.grade}")

student1 = Student("สมชาย", 3.5)
student1.print_info()