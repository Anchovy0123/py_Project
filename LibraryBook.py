class LibraryBook:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.available = True

    def checkout(self):
        if self.available:
            self.available = False
            print(f"ยืมหนังสือ: {self.title}")
        else:
            print(f"หนังสือ '{self.title}' ถูกยืมไปแล้ว")

    def checkin(self):
        self.available = True
        print(f"คืนหนังสือ: {self.title}")

# --- ทดสอบ ---
book = LibraryBook("Python 101", "นายโค้ด")
book.checkout()
book.checkout()   # จะขึ้นว่า ถูกยืมไปแล้ว
book.checkin()
