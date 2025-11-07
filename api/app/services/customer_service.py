from sqlalchemy.orm import Session

# models
from app.models.customer_model import Customer

# utils
# exceptions
from app.utils.exceptions import THROW_ERROR


"""
checkers
"""

# check if id exists
def check_id(id: int, db: Session) -> bool:
    customer = db.query(Customer).filter(Customer.id == id).first()
    if customer: True

    return False

# check if email are not in use
def check_email(email: str, db: Session) -> bool:
    customer = db.query(Customer).filter(Customer.email == email).first()
    if customer:
        return True
    
    return False

# check for phone
def check_phone(phone: str, db: Session) -> bool:
    customer = db.query(Customer).filter(Customer.phone == phone).first()
    if customer:
        return True
    
    return False


# check for nif
def check_nif(nif: str, db: Session) -> bool:
    customer = db.query(customer).filter(Customer.nif == nif).first()
    if customer:
        return True
    
    return False

"""
inserts | updates
"""

def insert_customer(data: dict, db: Session):

    new_customer = Customer(
        name = data["name"],
        email = data["email"],
        phone = data.get("phone"),
        nif = data.get("nif"),
        address = data.get("address"),
        country = data.get("country")
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer

def update_customer(customer_id: int,data: dict, db: Session):

    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    for key, value in data.items():
        setattr(customer, key, value)

    db.commit()
    db.refresh(customer)

    return customer

def inactive_customer(customer_id: int, db: Session):

    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    if customer.active is True:
        customer.active = False
    else:
        customer.active = True

    db.commit()
    db.refresh(customer)
    return customer

"""
gets
"""

def search_customer_variable(value: str, page: int, size: int, db: Session):

    query = db.query(Customer)
    offset = (page - 1) * size

    safe_value = value.replace("\\", "\\\\").replace("%", r"\%").replace("_", r"\_")
    # phone number
    digits = value.replace(" ", "").replace("+", "")
    phone = value.startswith("+") or digits.isdigit()

    # detect the type of the search

    # email
    if "@" in value:
        query = query.filter(Customer.email.ilike(f"{safe_value}%", escape="\\"))
    # phone number
    elif phone:
        query = query.filter(Customer.phone.ilike(f"{safe_value}%", escape="\\"))
    # NIF / tax ID
    elif value.isalnum():
        query = query.filter(Customer.nif.ilike(f"{safe_value}%", escape="\\"))
    # name
    else: 
        query = query.filter(Customer.name.ilike(f"%{safe_value}%", escape="\\"))

    results = query.order_by(Customer.created_at.desc()).limit(size).offset(offset).all()

    return results

def customers(db: Session):

    customers = db.query(Customer).filter(Customer.active == True).all()

    if not customers:
        THROW_ERROR("No customers", 400)

    return customers

def i_customers(db: Session):

    customers = db.query(Customer).filter(Customer.active == False).all()

    if not customers:
        THROW_ERROR("No inactive customers", 400)

    return customers


