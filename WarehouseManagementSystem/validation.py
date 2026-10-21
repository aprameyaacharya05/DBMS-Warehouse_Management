"""Small shared checks used before INSERT and UPDATE queries."""
from decimal import Decimal, InvalidOperation


def validate_values(data):
    for column, value in data.items():
        if value is None:
            continue  # Optional manager and supervisor IDs may be NULL.
        name = column.lower()
        integer = name.endswith(('_id', '_no', 'quantity')) or name == 'capacity'
        price = name in ('p_price', 'sell_price')
        if not integer and not price:
            continue
        text = str(value).strip()
        label = column.replace('_', ' ')
        if integer and (not text.isascii() or not text.isdigit()):
            raise ValueError(f'{label} must be a whole number, zero or greater.')
        if price:
            try:
                number = Decimal(text)
            except InvalidOperation:
                raise ValueError(f'{label} must be a valid price.') from None
            if not number.is_finite() or number < 0 or number.as_tuple().exponent < -2:
                raise ValueError(f'{label} must be zero or greater, with at most two decimal places.')
