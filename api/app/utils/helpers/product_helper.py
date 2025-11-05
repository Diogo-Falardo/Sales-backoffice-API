import re
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Optional
from pydantic import HttpUrl

# utils
# exceptions
from app.utils.exceptions import THROW_ERROR

def validate_sku(value: Optional[str]) -> str:
    if value is None:
        THROW_ERROR("SKU cannot be blank.", 400)
    if not isinstance(value, str):
        THROW_ERROR("SKU is not in the correct format", 400)

    sku = value.strip().upper()
    if not sku:
        THROW_ERROR("SKU cannot be empty.", 400)

    sku_regex = r"^[A-Za-z0-9][A-Za-z0-9_-]{2,99}$"
    if not re.fullmatch(sku_regex, sku):
        THROW_ERROR("SKU must be 3–100 chars, only letters, numbers, '-' or '_', and no spaces.", 400)

    return sku

def validate_price_cost(value: Optional[Decimal], title: str = "Amount") -> Decimal:
    if value is None:
        THROW_ERROR(f"{title} cannot be blank.", 400)

    try:
        value = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        THROW_ERROR(f"Invalid {title} format.", 400)

    if value < 0:
        THROW_ERROR(f"{title} must be a positive number.", 400)

    # round to 2 decimal places (financial rounding)
    value = value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # optional: prevent absurd prices
    if value > Decimal("9999999.99"):
        THROW_ERROR(f"{title} is too large.", 400)

    return value
    
def validate_stock(value: Optional[int]) -> int:
    if value is None:
        THROW_ERROR("Stock cannot be blank.", 400)
    if not isinstance(value, int):
        THROW_ERROR("Stock not in the correct format", 400)

    try:
        value = int(value)
    except (TypeError, ValueError):
        THROW_ERROR("Stock must be an integer.", 400)

    if value < 0:
        THROW_ERROR("Stock cannot be negative.", 400)
    if value > 1_000_000_000:
        THROW_ERROR("Stock value is too large.", 400)

    return value
    
def validate_description(value: Optional[str]) -> str:
    if value is None:
        THROW_ERROR("Product description cannot be blank.", 400)
    if not isinstance(value, str):
        THROW_ERROR("Product description is not in correct format", 400)

    product_description = value.strip()
    if not product_description:
        THROW_ERROR("Product description cannot be blank.", 400)

    if len(product_description) < 1:
        THROW_ERROR("Product description is too short.", 400)
        
    if len(product_description) > 1000:
        THROW_ERROR("Product description to long.", 400)

    if re.search(r"<[^>]+>", product_description):
        THROW_ERROR("Product description cannot contain HTML or script tags.", 400)

def validate_category(value: Optional[str]) -> str:
    if value is None:
        THROW_ERROR("Category cannot be blank.", 400)
    if not isinstance(value, str):
        THROW_ERROR("Category is not in correct format", 400)

    product_platform = value.strip()
    if not product_platform:
        THROW_ERROR("Category cannot be blank.", 400)

    if len(product_platform) < 2:
        THROW_ERROR("Category is too short.", 400)
    
    if len(product_platform) > 35:
        THROW_ERROR("Category platform is too Long.", 400)

def validate_img_url(value: Optional[str]) -> str:
    if value is None:
        return None

    try:
        url = HttpUrl(value)
        return str(url)
    except Exception:
        THROW_ERROR("Invalid URL format for img.", 400)
