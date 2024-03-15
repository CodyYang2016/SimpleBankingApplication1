import random
def generate_account_number(prefix: str, length: int = 10) -> str:
    """
    Generate a unique account number.

    :param prefix: The prefix for the account number, representing the bank and/or branch.
    :param length: The total length of the account number including the prefix and check digit.
    :return: A unique account number as a string.
    """
    if len(prefix) >= length - 1:
        raise ValueError("Prefix too long for the specified account number length.")
    
    # Generate the main body of the account number: random digits to fill up to the penultimate digit.
    main_length = length - len(prefix) - 1  # Subtract one for the check digit
    main_body = ''.join(str(random.randint(0, 9)) for _ in range(main_length))
    
    # Calculate a simple check digit: sum of digits modulo 10.
    digits = [int(d) for d in prefix + main_body]
    check_digit = sum(digits) % 10
    
    return f"{prefix}{main_body}{check_digit}"
