
import math


def parse_rental(text):
    if not isinstance(text, str):
        raise ValueError("Rental input must be a string")

    if text.count(':') != 1:
        raise ValueError("Input must be in unit:months format")

    unit, months = text.split(':')

    unit = unit.strip()

    if not unit:
        raise ValueError("Unit name cannot be empty")

    try:
        months = float(months)
    except (ValueError, TypeError):
        raise ValueError("Months must be a valid number")

    if not math.isfinite(months) or months < 0:
        raise ValueError("Months must be finite and non-negative")

    return unit.title(), months


def duration_average(months_csv):
    if not isinstance(months_csv, str) or not months_csv.strip():
        raise ValueError("Input must be a non-empty CSV string")

    parts = months_csv.split(',')

    values = []

    for item in parts:
        item = item.strip()

        if not item:
            raise ValueError("Empty duration entry is not allowed")

        try:
            value = int(item)
        except ValueError:
            raise ValueError("All durations must be integers")

        if value < 0:
            raise ValueError("Durations cannot be negative")

        values.append(value)

    return sum(values) // len(values)


def payable_rent(text):
    if not isinstance(text, str):
        raise ValueError("Rent input must be a string")

    if text.count('|') != 1:
        raise ValueError("Input must be in rent|discount format")

    rent, discount = text.split('|')

    try:
        rent = float(rent)
        discount = float(discount)
    except (ValueError, TypeError):
        raise ValueError("Rent and discount must be valid numbers")

    if not math.isfinite(rent) or not math.isfinite(discount):
        raise ValueError("Rent and discount must be finite numbers")

    if rent < 0:
        raise ValueError("Rent cannot be negative")

    if discount < 0:
        raise ValueError("Discount cannot be negative")

    total = rent * 1.18 - discount

    return max(total, 0)


def main():
    print("==== Running parse_rental ====")
    user_input = input("Enter unit:months (e.g. medium:6): ")
    result = parse_rental(user_input)
    print("Unit and Months:", result)

    print("\n==== Running duration_average ====")
    user_input = input("Enter rental months as CSV (e.g. 3,6,12): ")
    result = duration_average(user_input)
    print("Average Duration:", result)

    print("\n==== Running payable_rent ====")
    user_input = input("Enter rent|discount (e.g. 2400|200): ")
    result = payable_rent(user_input)
    print("Payable Rent:", result)


if __name__ == "__main__":
    main()
