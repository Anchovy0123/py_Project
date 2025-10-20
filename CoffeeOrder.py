class CoffeeOrder:
    def __init__(self, size, base_price):
        self.size = size
        self.base_price = base_price
        self.addons = []

    def add_addon(self, name):
        self.addons.append(name)

    def remove_addon(self, name):
        if name in self.addons:
            self.addons.remove(name)

    def num_addons(self):
        return len(self.addons)

    def total_price(self):
        return self.base_price + self.num_addons() * 10

# --- ทดสอบ ---
order = CoffeeOrder("Medium", 50)
order.add_addon("Extra Shot")
order.add_addon("Whipped Cream")
print(f"ขนาด: {order.size}")
print(f"Add-ons: {order.addons}")
print(f"จำนวน add-ons: {order.num_addons()}")
print(f"ราคารวม: {order.total_price()} บาท")
