#!/usr/bin/env python3
# coffee_cli.py — polished UI edition

import os, sys, time, datetime, random, re

# ---------- Enable ANSI colors on Windows ----------
def _enable_ansi_windows():
    if os.name != "nt":
        return
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
        mode = ctypes.c_uint32()
        kernel32.GetConsoleMode(handle, ctypes.byref(mode))
        kernel32.SetConsoleMode(handle, mode.value | 0x0004)  # ENABLE_VT_PROCESSING
    except Exception:
        pass
_enable_ansi_windows()

# ---------- Theme ----------
class Theme:
    enabled = True

class C:
    FG  = "\033[38;5;252m"  # primary text
    DIM = "\033[38;5;245m"  # dim text
    HI  = "\033[38;5;81m"   # cyan
    ACC = "\033[38;5;180m"  # caramel-ish
    OK  = "\033[38;5;113m"  # green
    WRN = "\033[38;5;214m"  # yellow
    ERR = "\033[38;5;203m"  # red
    EMP = "\033[38;5;255m"  # bright white
    BOX = "\033[38;5;240m"  # border
    MUT = "\033[38;5;237m"  # muted border
    RST = "\033[0m"

def col(s, color):
    return (color + s + C.RST) if Theme.enabled else s

def clear():
    os.system("cls" if os.name == "nt" else "clear")

# ---------- UI helpers ----------
WIDTH = 70

def hr(w=WIDTH):
    return col("─" * w, C.BOX)

def banner():
    cup = [
        "        (  )  (   ) )",
        "         ) (  )  (  (",
        "         ( ) (    ) )      ",
        "         _____________",
        "        <_____________> ___",
        "        |             |/ _ \\",
        "        |   COFFEE    | | | |",
        "        |    SHOP     | |_| |",
        "        |_____________|\\___/",
        "        \\_______________/    ",
    ]
    for line in cup:
        print(col(line.center(WIDTH), C.ACC if "COFFEE" in line or "SHOP" in line else C.DIM))

def pill(n):
    text = f" {n} "
    return col("", C.HI) + col(text, C.EMP) + col("", C.HI)

def titlebar(text):
    print()
    banner()
    print(hr())
    print(col(("  " + text + "  ").center(WIDTH), C.HI))
    print(hr())

def box(title=None):
    top = col("╭" + "─" * (WIDTH-2) + "╮", C.MUT)
    bot = col("╰" + "─" * (WIDTH-2) + "╯", C.MUT)
    if title:
        print(top)
        print(col(("  " + title + "  ").center(WIDTH), C.ACC))
        print(hr())
    else:
        print(top)
    return bot

def tip(text):  print(col("ⓘ " + text, C.DIM))
def ok(text):   print(col("✔ " + text, C.OK))
def warn(text): print(col("⚠ " + text, C.WRN))
def errm(text): print(col("✖ " + text, C.ERR))

def grid_menu(items, cols=1, pad=46):
    rows = (len(items) + cols - 1) // cols
    for r in range(rows):
        line = []
        for c in range(cols):
            i = r + c*rows
            if i < len(items):
                key, label = items[i]
                line.append(f"{pill(key)} {label}".ljust(pad))
        print("".join(line))
    print(hr())

def ask_line(prompt, default=None, allow_blank=False):
    suffix = f" [{default}]" if default is not None else ""
    v = input(col(f"{prompt}{suffix}: ", C.FG)).strip()
    if not v and default is not None: return default
    if not v and allow_blank: return ""
    return v

def ask_menu(prompt, valid_keys, default=None):
    keys = [str(k).upper() for k in valid_keys]
    while True:
        v = ask_line(prompt, default=default)
        v = (v or "").upper()
        if v in keys: return v
        if v in ("B", "Q"): return v
        warn("Invalid choice. Press 1/2/... (or 'b' back, 'q' exit).")

def pause(msg="Press Enter to continue..."):
    input(col(msg, C.DIM))

# ---------- Domain Model ----------
class CoffeeOrder:
    ADDON_PRICE = {"milk": 10, "choco": 15, "caramel": 15}

    def __init__(self, size="M", base_price=40.0, add_ons=None, qty=1, name="Custom"):
        self.size = size
        self.base_price = base_price
        self.add_ons = add_ons or []
        self.qty = qty
        self.name = name

    def _size_extra(self):
        return {"S": 0, "M": 5, "L": 10}.get(self.size, 0)

    def unit_price(self):
        addon_cost = sum(self.ADDON_PRICE.get(a, 0) for a in self.add_ons)
        return self.base_price + self._size_extra() + addon_cost

    def total_price(self):
        return self.unit_price() * self.qty

    def add_ons_text(self):
        return ", ".join(self.add_ons) if self.add_ons else "-"

# ---------- Data ----------
BASE_PRICE = 40.0
SIZES = [("S", 0), ("M", 5), ("L", 10)]
ADDONS_LIST = [("milk", 10), ("choco", 15), ("caramel", 15)]
PRESETS = [
    ("Americano",          "M", []),
    ("Espresso",           "S", []),
    ("Latte",              "M", ["milk"]),
    ("Cappuccino",         "M", ["milk"]),
    ("Flat White",         "M", ["milk"]),
    ("Mocha",              "M", ["milk", "choco"]),
    ("Choco Lover",        "L", ["choco"]),
    ("Caramel Latte",      "M", ["milk", "caramel"]),
    ("Caramel Macchiato",  "L", ["milk", "caramel"]),
    ("Caramel Mocha",      "L", ["milk", "choco", "caramel"]),
]

# ---------- Pickers ----------
def choose_size(default="M"):
    while True:
        clear(); titlebar("Choose Size")
        print(box()); rows_end = col("╰" + "─" * (WIDTH-2) + "╯", C.MUT)
        for i, (s, ex) in enumerate(SIZES, 1):
            tag = f"{s}  (+{ex} Baht)"
            if s == default: tag += col("  ← default", C.DIM)
            print(f"  {pill(i)} {tag}")
        print(rows_end)
        tip("Enter number, or 'b' to go back.")
        v = ask_line("Your choice")
        if v.lower() == "b": return None
        if v in ("1","2","3"): return SIZES[int(v)-1][0]
        warn("Please enter 1–3.")

def toggle_addons(current=None):
    selected = set(current or [])
    while True:
        clear(); titlebar("Choose Add-ons")
        print(box()); rows_end = col("╰" + "─" * (WIDTH-2) + "╯", C.MUT)
        for i, (name, price) in enumerate(ADDONS_LIST, 1):
            mark = col("●", C.ACC) if name in selected else col("○", C.DIM)
            print(f"  {pill(i)} [{mark}] {name:<8} {col(f'({price} Baht)', C.DIM)}")
        print(rows_end)
        tip("Toggle like 1,3  | Enter=Done  | 0=Clear  | b=Back")
        raw = ask_line("Your choice", allow_blank=True)
        if not raw: return sorted(selected)
        if raw.lower() == "b": return None
        raw = raw.replace(" ", "")
        if raw == "0":
            selected.clear(); continue
        try:
            idxs = [int(x) for x in raw.split(",") if x]
            if any(i < 1 or i > len(ADDONS_LIST) for i in idxs): raise ValueError
            for i in idxs:
                name = ADDONS_LIST[i-1][0]
                if name in selected: selected.remove(name)
                else: selected.add(name)
        except Exception:
            warn("Invalid input.")

def choose_qty(default=1):
    clear(); titlebar("Quantity")
    tip("Enter 1–20, or 'b' to back.")
    while True:
        raw = ask_line("Qty", default=str(default))
        if raw.lower() == "b": return None
        if raw.isdigit():
            n = int(raw)
            if 1 <= n <= 20: return n
        warn("Please enter 1–20.")

# ---------- Custom Builder ----------
def custom_builder(cart):
    size, addons, qty = "M", [], 1
    while True:
        clear(); titlebar("Add New Cup — Custom")
        unit = CoffeeOrder(size=size, base_price=BASE_PRICE, add_ons=addons).unit_price()
        b_end = box("Current selection")
        print(f"  • Size   : {col(size, C.EMP)}")
        print(f"  • Add-ons: {col(', '.join(addons) if addons else '-', C.EMP)}")
        print(f"  • Qty    : {col(str(qty), C.EMP)}")
        print(f"  • Unit   : {col(f'{unit:.2f} Baht', C.EMP)}")
        print(b_end)
        grid_menu([(1,"Change size"),(2,"Toggle add-ons"),(3,"Set quantity"),(4,"Add to cart"),(0,"Back")], cols=1)
        ch = ask_menu("Select", ["0","1","2","3","4"], default="4")
        if ch in ("0","B"): return
        if ch == "1":
            s = choose_size(default=size);  size = s or size
        elif ch == "2":
            a = toggle_addons(current=addons);  addons = a if a is not None else addons
        elif ch == "3":
            q = choose_qty(default=qty);  qty = q or qty
        elif ch == "4":
            cart.append(CoffeeOrder(size=size, base_price=BASE_PRICE, add_ons=addons, qty=qty))
            ok("Added to cart."); time.sleep(0.9); return

# ---------- Add New Cup (2 options) ----------
def add_new_cup_menu(cart):
    while True:
        clear(); titlebar("Add New Cup")
        grid_menu([(1,"Custom (builder)"),(2,"From presets (with optional tweaks)"),(0,"Back")], cols=1)
        ch = ask_menu("Select", ["0","1","2"], default="1")
        if ch in ("0","B"): return
        if ch == "1":
            custom_builder(cart)
        elif ch == "2":
            show_presets_for_add(cart)

# ---------- Presets ----------
def show_presets_for_add(cart):
    while True:
        clear(); titlebar("Presets")
        print(box()); rows_end = col("╰" + "─" * (WIDTH-2) + "╯", C.MUT)
        for i, (name, size, addons) in enumerate(PRESETS, 1):
            adds = ", ".join(addons) if addons else "-"
            unit = CoffeeOrder(size=size, base_price=BASE_PRICE, add_ons=addons).unit_price()
            print(f"  {pill(i)} {name:<18} | Size {size} | {adds:<22} | {col(f'{unit:>6.2f} Baht', C.EMP)}")
        print(f"  {pill(0)} Back")
        print(rows_end)
        pick = ask_line("Pick preset (number)", allow_blank=True)
        if not pick or pick == "0" or pick.lower()=="b": return
        if pick.isdigit() and 1 <= int(pick) <= len(PRESETS):
            idx = int(pick)-1
            name, def_size, def_addons = PRESETS[idx]
            use_def = ask_menu("Use default options? (Y/N)", ["Y","N"], default="Y")
            if use_def == "Y":
                size, addons = def_size, def_addons[:]
            else:
                s = choose_size(default=def_size);  size = s or def_size
                a = toggle_addons(current=def_addons); addons = a if a is not None else def_addons[:]
            q = choose_qty(default=1); qty = q or 1
            cart.append(CoffeeOrder(size=size, base_price=BASE_PRICE, add_ons=addons, qty=qty, name=name))
            ok(f"Added {name}."); time.sleep(0.9)
        else:
            warn("Invalid number.")

# ---------- Cart / Receipt / Checkout ----------
def zebra(i):  # alternate row color with faint border
    return C.MUT if i % 2 == 0 else C.BOX

def print_cart(cart):
    clear(); titlebar("Your Cart")
    if not cart:
        warn("Cart is empty."); print(hr()); return
    header = f"{'No.':<4} {'Item':<18} {'Size':<5} {'Add-ons':<20} {'Qty':>3} {'Unit':>8} {'Total':>10}"
    print(col(header, C.EMP)); print(hr())
    for i, it in enumerate(cart, 1):
        row = f"{i:<4} {it.name:<18} {it.size:<5} {it.add_ons_text():<20} {it.qty:>3} {it.unit_price():>8.2f} {it.total_price():>10.2f}"
        print(col(row, zebra(i)))
    print(hr())
    g = sum(i.total_price() for i in cart)
    print(col(f"{'Grand Total'.ljust(48)}{g:>12.2f} Baht", C.EMP))
    print(hr())

def strip_ansi(s): return re.sub(r"\x1b\[[0-9;]*m", "", s)

def make_receipt(cart):
    order_id = f"CF-{random.randint(100000, 999999)}"
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [hr(), col("RECEIPT".center(WIDTH), C.HI), hr()]
    lines.append(f"Order ID: {order_id}   Date: {ts}")
    lines.append(hr())
    lines.append(f"{'No.':<4} {'Item':<18} {'Size':<5} {'Add-ons':<20} {'Qty':>3} {'Unit':>8} {'Total':>10}")
    lines.append(hr())
    for i, o in enumerate(cart, 1):
        lines.append(f"{i:<4} {o.name:<18} {o.size:<5} {o.add_ons_text():<20} {o.qty:>3} {o.unit_price():>8.2f} {o.total_price():>10.2f}")
    lines.append(hr())
    grand = sum(o.total_price() for o in cart)
    lines.append(col(f"{'Grand Total:'.ljust(52)}{grand:>10.2f} Baht", C.EMP))
    lines.append(hr())
    return "\n".join(lines)

def checkout(cart):
    if not cart:
        warn("Cart is empty."); time.sleep(0.8); return
    print_cart(cart)
    go = ask_menu("Proceed to checkout? (Y/N)", ["Y","N"], default="Y")
    if go != "Y": return
    clear(); titlebar("Receipt")
    receipt = make_receipt(cart)
    print(receipt)
    save = ask_menu("Save receipt to file? (Y/N)", ["Y","N"], default="Y")
    if save == "Y":
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        name = f"coffee_receipt_{ts}.txt"
        with open(name, "w", encoding="utf-8") as f:
            f.write(strip_ansi(receipt))
        ok(f"Saved: {name}")
    ok("Thank you! Enjoy your coffee.")
    cart.clear()
    pause("Checkout complete. Press Enter to return to menu...")

# ---------- Main (4 items) ----------
def main():
    cart = []
    while True:
        clear(); titlebar("Coffee Order Program")
        tip(f"Base {BASE_PRICE:.2f} | Sizes S(+0) M(+5) L(+10) | Add-ons: milk(10) choco(15) caramel(15)")
        print()
        grid_menu([(1,"Add new cup"),(2,"View cart"),(3,"Checkout"),(4,"Exit")], cols=1)
        choice = ask_menu("Select", ["1","2","3","4"], default="1")
        if choice == "1": add_new_cup_menu(cart)
        elif choice == "2": print_cart(cart); pause()
        elif choice == "3": checkout(cart)
        elif choice in ("4","Q"): clear(); ok("Goodbye!"); return

# ---------- Presets used by Add new cup  ----------
# (kept above; no Quick presets entry point anymore)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye!")
        sys.exit(0)
