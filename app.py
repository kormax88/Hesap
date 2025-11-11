# app.py
from flask import Flask, request, jsonify, render_template
from calculator import calculate, CalculationError
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/calc", methods=["POST"])
def api_calc():
    """
    Beklenen JSON:
    {
      "op": "add" | "sub" | "mul" | "div" | "pow" | "sqrt" | "percent" | "neg",
      "a": "12.3",
      "b": "4.5"   # optional for unary ops
    }
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"ok": False, "error": "Geçersiz JSON."}), 400

    op = data.get("op")
    a = data.get("a")
    b = data.get("b")

    try:
        result = calculate(op, a, b)
        # Sonucu string olarak döndürelim (Decimal doğrudan JSON'a dönmez)
        return jsonify({"ok": True, "result": str(result)})
    except CalculationError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    except Exception as e:
        # beklenmeyen hata
        return jsonify({"ok": False, "error": "Sunucu hatası."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
