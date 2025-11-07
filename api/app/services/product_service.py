from sqlalchemy.orm import Session
from decimal import Decimal

# models
from app.models.product_model import Product

# utils
# exceptions
from app.utils.exceptions import THROW_ERROR

# schemas
from app.models.schemas.product_schema import StockHealthResponse, ShortProductInfo, StockValue

"""
checkers
"""

# check for product id
def check_id(id: int, db: Session) -> bool:
    product = db.query(Product).filter(Product.id == id).first()
    if product: return True

    return False

# check if sku is not in use
def check_sku(sku: str, db: Session) -> bool:
    product = db.query(Product).filter(Product.sku == sku).first()
    if product: return True

    return False



"""
inserts | updates
"""

def insert_product(data: dict, db: Session):

    new_product = Product(
        name = data["name"],
        sku = data["sku"],
        price = data["price"],
        stock = data["stock"],
        min_stock = data["min_stock"],
        description = data.get("description"),
        cost = data.get("cost"),
        category = data.get("category"),
        image_url = data.get("image_url")
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


def update_product(product_id, data: dict, db: Session):

    product = db.query(Product).filter(Product.id == id).first()

    for key, value in data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh()

    return product

def inactive_product(product_id: int, db: Session):

    product = db.query(Product).filter(Product.id == product_id).first()

    if product.active is True:
        product.active = False
    else:
        product.active = True

    db.commit()
    db.refresh(product)

    return product

def delete_product(product_id: int, db: Session):

    product = db.query(Product).filter(Product.id == product_id).first()

    db.delete(product)
    db.commit()

    return product

"""
gets
"""

def products(db: Session):

    products = db.query(Product).filter(Product.active == True).all()

    if not products:
        THROW_ERROR("No products", 400)


    return products

def i_products(db: Session):

    products = db.query(Product).filter(Product.active == False).all()

    if not products:
        THROW_ERROR("No inactive products", 400)

    return products

# stock management
def Mstock(threshold: int, db: Session) -> StockHealthResponse:

    product = db.query(Product).all()

    lowStock = []
    nearStock = []
    greenStock = []
    
    for products in product:
        if products.stock <= products.min_stock:
            lowStock.append(products)
        elif products.stock <= products.min_stock + threshold:
            nearStock.append(products)
        else:
            greenStock.append(products)

    totals = {
        "low": len(lowStock),
        "near": len(nearStock),
        "green": len(greenStock),
    }

    return StockHealthResponse(
        low_stock=[ShortProductInfo.model_validate(p) for p in lowStock],
        near_stock=[ShortProductInfo.model_validate(p) for p in nearStock],
        green=[ShortProductInfo.model_validate(p) for p in greenStock],
        totals=totals
    )

# stock value
def Vstock(db: Session) -> StockValue:

    product = db.query(Product).all()

    total_products = len(product)
    total_items = 0
    topLC = []
    midLC = []
    lowLC = []

    for products in product:
        total_items += products.stock
        total_value = products.stock * products.price
        total_cost = products.stock * products.cost
        total_profit = total_value - total_cost
        
        if products.cost > 0:
            margin = ((products.price - products.cost) / products.cost) * Decimal(100)
        else:
            margin = Decimal("inf")
        
        if margin >= 50:
            topLC.append(products)
        elif margin >= 20:
            midLC.append(products)
        else: 
            lowLC.append(products)


    return StockValue(
        total_products = total_products,
        total_items= total_items,
        total_value = total_value,
        total_cost = total_cost,
        total_profit = total_profit,
        top_lucrative_products = [ShortProductInfo.model_validate(p) for p in topLC],
        mid_lucrative_products = [ShortProductInfo.model_validate(p) for p in midLC],
        low_lucrative_products = [ShortProductInfo.model_validate(p) for p in lowLC]
    )
            


