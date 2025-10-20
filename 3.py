class Classroom:
    def __init__(self, class_name, teacher, subject, max_students):
        self.class_name = class_name           
        self.teacher = teacher                 
        self.subject = subject                 
        self.max_students = max_students      
        self.students = {}                      

    def _level(self, s):
        """คืนชื่อระดับชั้นจาก student (ถ้ามี calculate_grade_level() ใช้ได้เลย, ไม่งั้นคำนวณจากอายุ)"""
        if hasattr(s, "calculate_grade_level") and callable(s.calculate_grade_level):
            return s.calculate_grade_level()
        age = getattr(s, "age", None)
        if age is None: return "ไม่ทราบระดับชั้น"
        if age < 13: return "ประถมศึกษา"
        if age < 16: return "มัธยมต้น"
        if age < 19: return "มัธยมปลาย / ปวช."
        if age < 22: return "อุดมศึกษา"
        return "บุคคลทั่วไป / ศึกษาต่อ"

    def add_student(self, student):
        """เพิ่มนักเรียนเข้าห้อง (กันซ้ำ/กันห้องเต็ม)"""
        if self.is_class_full():
            print("เพิ่มไม่สำเร็จ: ห้องเรียนเต็ม")
            return False
        sid = getattr(student, "student_id", None)
        if not sid:
            print("เพิ่มไม่สำเร็จ: student ไม่มี student_id")
            return False
        if sid in self.students:
            print(f"เพิ่มไม่สำเร็จ: มีรหัส {sid} แล้ว")
            return False
        self.students[sid] = student
        return True

    def remove_student(self, student_id):
        """ลบนักเรียนออกจากห้อง (คืน object ที่ถูกลบ หรือ None ถ้าไม่พบ)"""
        return self.students.pop(student_id, None)

    def find_student(self, student_id):
        """ค้นหานักเรียนโดยรหัส (คืน object หรือ None)"""
        return self.students.get(student_id)

    def get_class_size(self):
        """จำนวนผู้เรียนปัจจุบัน"""
        return len(self.students)

    def is_class_full(self):
        """ตรวจสอบว่าเต็มหรือยัง"""
        return self.get_class_size() >= self.max_students

    def get_students_by_grade_level(self, level):
        """คืน list นักเรียนที่ระดับชั้นตรงกับ level"""
        return [s for s in self.students.values() if self._level(s) == level]

    def calculate_average_grade(self):
        """คำนวณเกรดเฉลี่ยของห้อง (เฉลี่ยจากแอททริบิวต์ s.grade)"""
        grades = [
            float(getattr(s, "grade", float("nan")))
            for s in self.students.values()
            if isinstance(getattr(s, "grade", None), (int, float))
        ]
        return sum(grades) / len(grades) if grades else 0.0

    def display_class_info(self):
        """แสดงข้อมูลห้องเรียน"""
        print("=== ข้อมูลห้องเรียน ===")
        print(f"ห้องเรียน : {self.class_name}")
        print(f"ครูประจำชั้น : {self.teacher}")
        print(f"วิชาที่สอน : {self.subject}")
        print(f"นักเรียน : {self.get_class_size()} / {self.max_students}")
        print(f"เกรดเฉลี่ยห้อง : {self.calculate_average_grade():.2f}")
        print("รายชื่อนักเรียน:")
        if not self.students:
            print("  - (ยังไม่มีนักเรียน)")
        else:
            for s in self.students.values():
                sid = getattr(s, "student_id", "-")
                name = getattr(s, "name", "-")
                age = getattr(s, "age", "-")
                grade = getattr(s, "grade", "-")
                print(f"  - {sid} | {name} | อายุ {age} | เกรด {grade} | {self._level(s)}")
        print("======================")

    def rank_students(self, order="desc", top=None):
        """
        คืน list ของ tuple (student, grade) เรียงตามเกรด
        order: 'desc' มาก->น้อย (ค่าเริ่มต้น) หรือ 'asc' น้อย->มาก
        top: จำนวนบนสุดที่ต้องการ (None = ทั้งหมด)
        """
        data = [
            (s, float(getattr(s, "grade", float("-inf"))))
            for s in self.students.values()
        ]
        data.sort(key=lambda x: x[1], reverse=(order == "desc"))
        return data[:top] if isinstance(top, int) and top > 0 else data

    def display_ranking(self, order="desc", top=None):
        """พิมพ์ตารางจัดอันดับนักเรียนตามเกรด"""
        ranked = self.rank_students(order, top)
        print("=== จัดอันดับนักเรียนตามเกรด ===")
        if not ranked:
            print("(ไม่มีข้อมูลนักเรียน)")
        else:
            for i, (s, g) in enumerate(ranked, 1):
                print(f"{i:>2}. {getattr(s,'student_id','-')} | {getattr(s,'name','-')} | เกรด {g:.2f}")
        print("=============================")

if __name__ == "__main__":

    class StudentDemo:
        def __init__(self, student_id, name, age, grade):
            self.student_id, self.name, self.age, self.grade = student_id, name, age, grade
        def calculate_grade_level(self):
            if self.age < 13: return "ประถมศึกษา"
            if self.age < 16: return "มัธยมต้น"
            if self.age < 19: return "มัธยมปลาย / ปวช."
            if self.age < 22: return "อุดมศึกษา"
            return "บุคคลทั่วไป / ศึกษาต่อ"

    cls = Classroom("IT101", "ครูพิมพ์", "โปรแกรมมิ่งเบื้องต้น", 5)

    for s in [
        StudentDemo("ST001","สมชาย ใจดี",20,3.00),
        StudentDemo("ST002","สมศรี สายเรียน",19,3.75),
        StudentDemo("ST003","ชลธิชา ตั้งใจ",21,2.10),
        StudentDemo("ST004","ปิยะพงษ์ ขยัน",18,4.00),
    ]:
        cls.add_student(s)

    cls.display_class_info()

    print("ค้นหา ST003 ->", getattr(cls.find_student("ST003"), "name", None))
    print("ห้องเต็มหรือไม่ ->", cls.is_class_full())
    cls.remove_student("ST003")
    print("หลังลบ ST003 ->", cls.get_class_size(), "คน")

    uni = cls.get_students_by_grade_level("อุดมศึกษา")
    print("นักศึกษา 'อุดมศึกษา':", [s.name for s in uni])

    cls.display_ranking(order="desc", top=3)
