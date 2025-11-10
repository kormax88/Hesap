from flask import Flask, render_template, request, jsonify
import ast
from decimal import Decimal, getcontext

# Daha yüksek hassasiyet gerekiyorsa ayarla:
getcontext().prec = 28

app = Flask(__name__)

# Güvenli AST tabanlı evaluator
ALLOWED_BINOPS = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod, ast.FloorDiv)
ALLOWED_UNARYOPS = (ast.UAdd, ast.USub)
ALLOWED_NODES = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant, ast.Call, ast.Name, ast.Load, ast.Tuple)

# İzin verilen isimli fonksiyonlar (opsiyonel, burada yok)
SAFE_NAMES = {}

def safe_eval(expr: str):
    """
    Basit matematiksel ifadeleri güvenli şekilde değerlendirir.
    İzin verilen: + - * / ** % // parantez, sayılar.
    Hatalı veya izin verilmeyen node gelirse ValueError fırlatır.
    """
    try:
        node = ast.parse(expr, mode='eval')
    except Exception as e:
        raise ValueError("Geçersiz ifade")

    def _eval(n):
        if isinstance(n, ast.Expression):
            return _eval(n.body)
        if isinstance(n, ast.BinOp):
            left = _eval(n.left)
            right = _eval(n.right)
            op = n.op
            if isinstance(op, ast.Add):
                return left + right
            if isinstance(op, ast.Sub):
                return left - right
            if isinstance(op, ast.Mult):
                return left * right
            if isinstance(op, ast.Div):
                # Decimal bölme (sıfıra bölme kontrolü)
                if right == Decimal(0):
                    raise ValueError("Sıfıra bölme")
                return left / right
            if isinstance(op, ast.FloorDiv):
                if right == Decimal(0):
                    raise ValueError("Sıfıra bölme")
                return left // right
            if isinstance(op, ast.Mod):
                if right == Decimal(0):
                    raise ValueError("Sıfıra bölme")
                return left % right
            if isinstance(op, ast.Pow):
                # Be careful with huge exponents — Decimal kullan ve izin ver
                # float riskini azaltmak için exponenti integer'a çevirebiliriz
                # (burada küçük sayılar için normal çalışır)
                return left ** right
            raise ValueError("İzin verilmeyen işlem")
        if isinstance(n, ast.UnaryOp):
            operand = _eval(n.operand)
            if isinstance(n.op, ast.UAdd):
                return +operand
            if isinstance(n.op, ast.USub):
                return -operand
            raise ValueError("İzin verilmeyen unary operatör")
        if isinstance(n, ast.Num):  # Python <3.8
            return Decimal(str(n.n))
        if isinstance(n, ast.Constant):  # Python 3.8+
            if isinstance(n.value, (int, float)):
                return Decimal(str(n.value))
            raise ValueError("Sadece sayılar izinli")
        # Diğer node'lar yasak
        raise ValueError("İzin verilmeyen ifade parçasi")

    result = _eval(node)
    return result

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/eval", methods=["POST"])
def evaluate():
    data = request.get_json(force=True)
    expr = data.get("expr", "")
    if not isinstance(expr, str) or expr.strip() == "":
        return jsonify({"error": "Boş ifade"}), 400
    try:
        res = safe_eval(expr)
        # Decimal -> string (kayıpsız)
        return jsonify({"result": format(res, 'f')})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Hesaplama hatası"}), 400

if __name__ == "__main__":
    # Geliştirme için
    app.run(host="0.0.0.0", port=5000, debug=True)
