from sqlalchemy.orm import Session
from decimal import Decimal
import enum

# models
from app.models.order_model import Order, OrderItem

# utils
# exceptions
from app.utils.exceptions import THROW_ERROR

# schemas
from app.models.schemas.order_schema import OrderCreate, OrderStatusUpdate, OrderOut

"""
checkers
"""

def check_order_id(order_id: int, db: Session):
    # return order to faster progress
    order = db.query(Order).filter(Order.id == order_id).first()
    if order: return order

    return None

"""
inserts | updates
"""

def insert_order(payload: OrderCreate, db: Session):
    order = Order()
    db.add(order)
    db.flush() # order_id

    subtotal = Decimal("0.00")

    for item in payload.items:
        line_total = Decimal(item.qty) * Decimal(item.unit_price)
        subtotal += line_total
        order_item = OrderItem(
            order_id = order.id,
            product_id = item.product_id,
            qty = item.qty,
            unit_price =  item.unit_price,
            line_total = line_total,
        )

        db.add(order_item)

    order.subtotal = subtotal
    # in future -> add taxes etc.. etc..
    order.total = subtotal

    db.commit()
    db.refresh(order)
    return order

# update status
def update_order_status(payload: OrderStatusUpdate, db: Session):

    order = check_order_id(payload.order_id, db)

    if not order:
        THROW_ERROR("Order not found", 404)


    order.status = payload.status
    db.commit()
    db.refresh(order)

    return order

"""
get
"""
class OrderStatus(str, enum.Enum):
    draft = "draft"
    paid = "paid"
    shipped = "shipped"
    cancelled = "cancelled"


def order_by_status(db: Session):

    orders = db.query(Order).all()

    if not orders:
        THROW_ERROR("Order not found", 404)

    draft, paid, shipped, cancelled = [], [], [], []

    for order in orders:
        if order.status == OrderStatus.draft:
            draft.append(order)
        elif order.status == OrderStatus.paid:
            paid.append(order)
        elif order.status == OrderStatus.shipped:
            shipped.append(order)
        elif order.status == OrderStatus.cancelled:
            cancelled.append(order)

    totals = {
        "draft": len(draft),
        "paid": len(paid),
        "shipped": len(shipped),
        "cancelled": len(cancelled),
    }

    return {
        "draft": [OrderOut.model_validate(o) for o in draft],
        "paid": [OrderOut.model_validate(o) for o in paid],
        "shipped": [OrderOut.model_validate(o) for o in shipped],
        "cancelled": [OrderOut.model_validate(o) for o in cancelled],
        "totals": totals
    }    