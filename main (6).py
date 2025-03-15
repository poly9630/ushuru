
# MN Income Tax Rate for different filing statuses (2023)
tax_brackets = {
    'single': [
        (0.0535, 31960),
        (0.068, 104090),
        (0.0785, 193240),
        (0.0985, float('inf'))
    ],
    'married': [
        (0.0535, 46620),
        (0.068, 165430),
        (0.0785, 276200),
        (0.0985, float('inf'))
    ]
}

def get_valid_input(prompt, input_type=float, valid_options=None):
    while True:
        try:
            user_input = input(prompt)
            if input_type == str and valid_options:
                if user_input.lower() in valid_options:
                    return user_input.lower()
                raise ValueError
            return input_type(user_input)
        except ValueError:
            if valid_options:
                print(f"Invalid input. Please enter one of: {', '.join(valid_options)}")
            else:
                print(f"Invalid input. Please enter a valid {input_type.__name__}")

def calculate_tax(income, filing_status, dependents):
    # Basic deduction based on dependents ($4,450 per dependent in MN)
    dependent_deduction = dependents * 4450
    taxable_income = max(0, income - dependent_deduction)
    
    brackets = tax_brackets[filing_status]
    total_tax = 0
    bracket_taxes = []
    remaining_income = taxable_income

    for rate, threshold in brackets:
        if remaining_income <= 0:
            bracket_taxes.append((rate * 100, 0))
        elif remaining_income <= threshold:
            tax = remaining_income * rate
            bracket_taxes.append((rate * 100, tax))
            total_tax += tax
            remaining_income = 0
        else:
            tax = threshold * rate
            bracket_taxes.append((rate * 100, tax))
            total_tax += tax
            remaining_income -= threshold

    return total_tax, bracket_taxes, dependent_deduction

def main():
    # Get user details
    income = get_valid_input("Enter your annual income: $")
    filing_status = get_valid_input("Enter filing status (single/married): ", str, ['single', 'married'])
    dependents = get_valid_input("Enter number of dependents: ", int)

    # Calculate taxes
    total_tax, bracket_taxes, dependent_deduction = calculate_tax(income, filing_status, dependents)

    # Print results
    print(f"\nFiling Status: {filing_status.capitalize()}")
    print(f"Number of Dependents: {dependents}")
    print(f"Dependent Deduction: ${dependent_deduction:,.2f}")
    print(f"Taxable Income: ${max(0, income - dependent_deduction):,.2f}")
    print(f"\nYou owe a total MN income tax of: ${total_tax:,.2f} before any additional deductions.\n")

    for rate, tax in bracket_taxes:
        print(f"{rate:.2f}% bracket: ${tax:,.2f}")

if __name__ == "__main__":
    main()
