# Expense Tracker (console) — phone-friendly
# Run in Replit (main.py) or Pydroid (expense_tracker.py)
from datetime import date, datetime
from pathlib import Path
from collections import defaultdict
import csv

DATA_FILE = Path("expenses.csv")
DEFAULT_CATEGORIES = ["Food", "Transport", "Bills", "Entertainment", "Shopping", "Health", "Other"]

# ---------- Storage ----------
def load_expenses(csv_path: Path):
    rows = []
    if not csv_path.exists():
        return rows
    with csv_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                amt = float(r.get("amount", "0") or 0)
            except ValueError:
                amt = 0.0
            rows.append({
                "date": r.get("date", ""),
                "amount": amt,
                "category": r.get("category", ""),
                "note": r.get("note", "")
            })
    return rows

def save_expenses(csv_path: Path, expenses):
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "amount", "category", "note"])
        writer.writeheader()
        for e in expenses:
            writer.writerow({
                "date": e["date"],
                "amount": f"{e['amount']:.2f}",
                "category": e["category"],
                "note": e["note"]
            })

# ---------- Utilities ----------
def input_with_default(prompt, default_value=None):
    suffix = f" [{default_value}]" if default_value is not None else ""
    s = input(prompt + suffix + ": ").strip()
    return default_value if (s == "" and default_value is not None) else s

def parse_date(s):
    # Accept YYYY-MM-DD; Enter = today
    if not s:
        return date.today().isoformat()
    try:
        d = datetime.strptime(s, "%Y-%m-%d").date()
        return d.isoformat()
    except ValueError:
        print("❗ Please use YYYY-MM-DD (e.g., 2025-09-01).")
        return None

def parse_amount(s):
    try:
        amt = float(s)
        if amt <= 0:
            print("❗ Amount must be > 0.")
            return None
        return round(amt, 2)
    except ValueError:
        print("❗ Enter a valid number (e.g., 199.99).")
        return None

def pick_category():
    print("\nChoose a category:")
    for i, c in enumerate(DEFAULT_CATEGORIES, start=1):
        print(f"  {i}. {c}")
    print("  0. Custom")
    choice = input("Enter number (or type name): ").strip()
    if choice.isdigit():
        n = int(choice)
        if n == 0:
            name = input("Type custom category: ").strip()
            return name if name else "Other"
        if 1 <= n <= len(DEFAULT_CATEGORIES):
            return DEFAULT_CATEGORIES[n - 1]
    # If user typed a name directly
    return choice if choice else "Other"

# ---------- Actions ----------
def add_expense_flow(expenses):
    print("\n➕ Add Expense")
    while True:
        d = parse_date(input_with_default("Date (YYYY-MM-DD)", date.today().isoformat()))
        if d: break
    while True:
        amt = parse_amount(input("Amount: ").strip())
        if amt is not None: break
    cat = pick_category()
    note = input("Note (optional): ").strip()
    expenses.append({"date": d, "amount": amt, "category": cat, "note": note})
    save_expenses(DATA_FILE, expenses)
    print("✅ Saved.")

def list_expenses(expenses):
    print("\n📄 Your Expenses (latest first)")
    if not expenses:
        print("No expenses yet.")
        return
    total = 0.0
    for idx, e in enumerate(reversed(expenses), start=1):
        total += e["amount"]
        print(f"{idx}. {e['date']}  ₹{e['amount']:.2f}  [{e['category']}]  {e['note']}")
    print(f"— Total: ₹{total:.2f} ({len(expenses)} items)")

def report_by_category(expenses):
    print("\n📊 Totals by Category")
    if not expenses:
        print("No data yet.")
        return
    totals = defaultdict(float)
    for e in expenses:
        totals[e["category"]] += e["amount"]
    grand = 0.0
    for cat, amt in sorted(totals.items(), key=lambda x: -x[1]):
        grand += amt
        print(f"- {cat}: ₹{amt:.2f}")
    print(f"— Grand Total: ₹{grand:.2f}")

# ---------- Main Menu ----------
def main():
    expenses = load_expenses(DATA_FILE)
    while True:
        print("\n==== Expense Tracker ====")
        print("1) Add expense")
        print("2) List expenses")
        print("3) Report by category")
        print("4) Save (backup) now")
        print("0) Exit")
        choice = input("Select: ").strip()
        if choice == "1":
            add_expense_flow(expenses)
        elif choice == "2":
            list_expenses(expenses)
        elif choice == "3":
            report_by_category(expenses)
        elif choice == "4":
            save_expenses(DATA_FILE, expenses)
            print("💾 Saved.")
        elif choice == "0":
            save_expenses(DATA_FILE, expenses)
            print("👋 Bye!")
            break
        else:
            print("❗ Invalid choice. Try 0–4.")

if __name__ == "__main__":
    main()