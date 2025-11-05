import re
from typing import Optional

# utils
# exceptions
from app.utils.exceptions import THROW_ERROR

"""
input validators
"""

def validate_name(value: Optional[str]) -> str:
    if value is None:
        THROW_ERROR("Name cannot be blank.", 400)
    if not isinstance(value, str):
        THROW_ERROR("Name is not in the correct format", 400)

    name = value.strip()
    if not name:
        THROW_ERROR("Name cannot be blank.", 400)

    if len(name) < 3:
        THROW_ERROR("Name is to short.", 400)
    if len(name) > 100:
        THROW_ERROR("Name is to long.", 400)

    regex = r"^[A-Za-z0-9 ]*[A-Za-z0-9][A-Za-z0-9 ]*$"
    if not re.fullmatch(regex, name):
        THROW_ERROR("Name must contain only letters, numbers, and spaces")

    return name

def validate_phone(value: Optional[str]) -> str:
    if value is None:
        THROW_ERROR("Phone number cannot be blank.", 400)
    if not isinstance(value, str):
        THROW_ERROR("Phone number is not in the correct format", 400)

    phone_number = value.strip()
    if not phone_number:
        THROW_ERROR("Phone number cannot be blank.", 400)

    if len(phone_number) < 5:
        THROW_ERROR("Phone number is to short.", 400)
    if len(phone_number) > 50:
        THROW_ERROR("Phone number is to long.", 400)

    regex = r"^[0-9+ ]+$"
    if not re.fullmatch(regex, phone_number):
        THROW_ERROR("Phone number can only contain digits, spaces and '+'.", 400)
    
    return phone_number

def validate_nif(value: Optional[str]) -> str:
    if value is None:
        THROW_ERROR("NIF/Tax ID cannot be blank.", 400)
    if not isinstance(value, str):
        THROW_ERROR("NIF/Tax ID is not in the correct format", 400)

    nif = value.strip().upper()
    if not nif:
        THROW_ERROR("NIF/Tax ID cannot be blank.", 400)
    
    if len(nif) < 5:
        THROW_ERROR("NIF/Tax ID is too short.", 400)
    if len(nif) > 20:
        THROW_ERROR("NIF/Tax ID is too long.", 400)

    regex = r"^[A-Za-z0-9]+$"
    if not re.fullmatch(regex, nif):
        THROW_ERROR("Tax ID can only contain letters and numbers.", 400)

    return nif

def validate_address(value: Optional[str]) -> str:
    if value is None:
        THROW_ERROR("Address cannot be blank.", 400)
    if not isinstance(value, str):
        THROW_ERROR("Address is not in the correct format", 400)

    address = value.strip()
    if not address:
        THROW_ERROR("Address cannot be blank.", 400)

    if len(address) < 5:
        raise ValueError("Address is too short.")
    if len(address) > 200:
        raise ValueError("Address is too long.")
    
    address_regex = r"^[A-Za-zÀ-ÿ0-9\s.,'ºª\-/#()]+$"
    if not re.fullmatch(address_regex, value):
        raise ValueError("Address contains invalid characters.")
    
    return address

def validate_country(value: Optional[str]) -> str:
    if value is None:
        THROW_ERROR("Country name cannot be blank.", 400)
    if not isinstance(value, str):
        THROW_ERROR("Country name is not in the correct format", 400)

    country = value.strip().title
    
    if len(country) < 2:
        raise ValueError("Country name is too short.")
    if len(country) > 60:
        raise ValueError("Country name is too long.")

    if not re.fullmatch(r"^[A-Za-zÀ-ÿ\s\-]+$", country):
        THROW_ERROR("Country name must contain only letters and spaces.", 400)



        