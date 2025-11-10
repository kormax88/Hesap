from calculator_cli import add, sub, mul, div, power, sqrt
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Hesap Makinesi API Çalışıyor ✅"

@app.route("/calc", methods=["GET"])
def calc():
    op = request.args.get("op")
    a = float(request.args.get("a", 0))
    b = request.args.get("b")

    if op == "add":
        return jsonify(result=add(a, float(b)))
    elif op == "sub":
        return jsonify(result=sub(a, float(b)))
    elif op == "mul":
        return jsonify(result=mul(a, float(b)))
    elif op == "div":
        return jsonify(result=div(a, float(b)))
    elif op == "power":
        return jsonify(result=power(a, float(b)))
    elif op == "sqrt":
        return jsonify(result=sqrt(a))
    else:
        return jsonify(error="Geçersiz işlem")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
