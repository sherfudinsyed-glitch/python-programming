from decimal import Decimal
import milkrate as mr

# --- Rate tests: both seasons ---
assert mr.rate_per_litre("3.50", "8.50", "normal") == Decimal("30.00")
assert mr.rate_per_litre("3.50", "8.50", "summer") == Decimal("32.00")
assert mr.rate_per_litre("4.23", "8.67", "normal") == Decimal("33.43")   # 30+2.92+0.51
assert mr.rate_per_litre("4.23", "8.67", "summer") == Decimal("35.80")   # 32+3.285+0.51 = 35.795 -> 35.80
assert mr.rate_per_litre("3.10", "8.30", "normal") == Decimal("27.80")

# --- Season selection ---
assert mr.season_for_month(4) == "summer"
assert mr.season_for_month(6) == "summer"
assert mr.season_for_month(7) == "normal"

# --- Bonus tests (boundary: exactly 500 gets no bonus) ---
assert mr.bonus(500) == Decimal("0.00")
assert mr.bonus(500.5) == Decimal("250.25")
assert mr.bonus(620) == Decimal("310.00")

# --- Ten-day totals ---
small = [(10, "3.50", "8.50")] * 10                     # 100 L, no bonus
amt, b, grand = mr.ten_day_total(small, "normal")
assert (amt, b, grand) == (Decimal("3000.00"), Decimal("0.00"), Decimal("3000.00"))

large = [(60, "3.50", "8.50")] * 10                     # 600 L, bonus applies
amt, b, grand = mr.ten_day_total(large, "summer")
assert (amt, b, grand) == (Decimal("19200.00"), Decimal("300.00"), Decimal("19500.00"))

print("All tests passed")
print("Old design (round steps) for 4.23/8.67 normal:",
      round(30 + round((4.23 - 3.5) / 0.1) * 0.40 + round((8.67 - 8.5) / 0.1) * 0.30, 2))
print("New design for 4.23/8.67 normal:", mr.rate_per_litre("4.23", "8.67", "normal"))
