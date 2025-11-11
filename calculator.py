# calculator.py
from decimal import Decimal, getcontext, DivisionByZero, InvalidOperation, ROUND_HALF_EVEN
import math

# Hassasiyeti ayarla (gerektiğinde artırabilirsin)
getcontext().prec = 28
getcontext().rounding = ROUND_HALF_EVEN

class CalculationError(Exception):
    pass

def _to_decimal(value):
    """
    Gelen değeri güvenli şekilde Decimal'e çevirir.
    Kabul eder: string, int, float (float önce string'e çevrilir).
    Virgül (',') olursa noktaya çevirir.
    """
    if isinstance(value, str):
        s = value.strip().replace(',', '.')
    elif isinstance(value, float):
        # float doğrudan Decimal'e çevirmek hassasiyet kaybettirir;
        # bunun için float'ı string'e çeviriyoruz.
        s = format(value, 'g')
    elif isinstance(value, (int, Decimal)):
        return Decimal(value)
    else:
        raise CalculationError("Desteklenmeyen sayı tipi.")
    try:
        return Decimal(s)
    except (InvalidOperation, ValueError):
        raise CalculationError(f"Geçersiz sayı: {value!r}")

def add(a, b):
    return _to_decimal(a) + _to_decimal(b)

def sub(a, b):
    return _to_decimal(a) - _to_decimal(b)

def mul(a, b):
    return _to_decimal(a) * _to_decimal(b)

def div(a, b):
    da = _to_decimal(a)
    db = _to_decimal(b)
    try:
        return da / db
    except DivisionByZero:
        raise CalculationError("Sıfıra bölme hatası.")

def power(a, b):
    # Decimal.pow sınırlamaları olduğu için float üssü kabul edip güvenli şekilde yapıyoruz
    da = _to_decimal(a)
    db = _to_decimal(b)
    # Eğer üs tam sayıysa doğrudan kullan
    try:
        if db == db.to_integral_value():
            return da ** int(db)
        # non-integer exponents -> convert to float for math.pow then back to Decimal
        res = Decimal(str(float(da) ** float(db)))
        return res
    except (InvalidOperation, OverflowError):
        raise CalculationError("Üs hesaplanamadı.")

def sqrt(a):
    da = _to_decimal(a)
    if da < 0:
        raise CalculationError("Negatif sayının karekökü alınamaz.")
    # Decimal.sqrt olabilir, ama python sürümüne göre kullanılmayabilir; güvenli yol:
    return Decimal(str(math.sqrt(float(da))))

def percent(a):  # yüzde değerini döndürür (ör: %10 için 0.1)
    return _to_decimal(a) / Decimal(100)

def negate(a):
    return -_to_decimal(a)

# Basit expression yerine operatör tabanlı API kullanıyoruz.
OPERATIONS = {
    "add": add,
    "sub": sub,
    "mul": mul,
    "div": div,
    "pow": power,
    "sqrt": sqrt,
    "percent": percent,
    "neg": negate
}

def calculate(op, a=None, b=None):
    """
    op: 'add','sub','mul','div','pow','sqrt','percent','neg'
    a, b: operandlar (string/int/float)
    """
    if op not in OPERATIONS:
        raise CalculationError("Geçersiz işlem.")
    func = OPERATIONS[op]
    # unary ops
    if op in ("sqrt", "percent", "neg"):
        if a is None:
            raise CalculationError("Operand eksik.")
        return func(a)
    # binary ops
    if a is None or b is None:
        raise CalculationError("Operand eksik.")
    return func(a, b)
