from calculator_cli import add, sub, mul, div, power, sqrt
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Hesap Makinesi Web API Çalışıyor"

@app.route("/hesap")
def hesap():
    op = request.args.get("op")
    a = float(request.args.get("a", 0))
    b = request.args.get("b")

    try:
        if op == "add":
            return str(add(a, float(b)))
        elif op == "sub":
            return str(sub(a, float(b)))
        elif op == "mul":
            return str(mul(a, float(b)))
        elif op == "div":
            return str(div(a, float(b)))
        elif op == "power":
            return str(power(a, float(b)))
        elif op == "sqrt":
            return str(sqrt(a))
        else:
            return "Geçersiz işlem"
    except Exception as e:
        return "Hata: " + str(e)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
