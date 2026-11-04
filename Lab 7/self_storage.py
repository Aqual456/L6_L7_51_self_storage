def parse_rental(text):
    unit, months = text.split(':')
    return unit.strip().title(), float(months)

def duration_average(months_csv):
    values = [int(r) for r in months_csv.split(',')]
    return sum(values) // len(values)

def payable_rent(text):
    rent, discount = text.split('|')
    total = float(rent) * 1.18 - float(discount)
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
