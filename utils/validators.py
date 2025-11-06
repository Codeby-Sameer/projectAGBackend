def is_valid_phone(value: str) -> bool:
    return value.isdigit() or value.startswith('+')



def is_valid_aadhar(value: str) -> bool:
    return value.isdigit() and len(value) == 12

def is_valid_contact(value: str) -> bool:
    return value.isdigit() and len(value) == 10
