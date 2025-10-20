class StudentPlus:
    def __init__(self, name, scores):
        self.name = name
        self.scores = scores

    def average(self):
        return sum(self.scores) / len(self.scores)

    def grade(self):
        avg = self.average()
        if avg >= 80:
            return "A"
        elif avg >= 70:
            return "B"
        elif avg >= 60:
            return "C"
        elif avg >= 50:
            return "D"
        else:
            return "F"

    @property
    def passed(self):
        return self.average() >= 50

# --- ทดสอบ ---
s1 = StudentPlus("สมชาย", [80, 75, 90])
s2 = StudentPlus("สายฝน", [45, 60, 55])

for s in [s1, s2]:
    print(f"ชื่อ: {s.name}")
    print(f"คะแนนเฉลี่ย: {s.average():.2f}")
    print(f"เกรด: {s.grade()}")
    print(f"ผ่าน: {s.passed}")
    print("-" * 20)
