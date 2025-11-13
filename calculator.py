from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        try:
            number1 = float(request.form["number1"])
            number2 = float(request.form["number2"])
            operation = request.form["operation"]

            if operation == "toplama":
                result = number1 + number2
            elif operation == "cikarma":
                result = number1 - number2
            elif operation == "carpma":
                result = number1 * number2
            elif operation == "bolme":
                if number2 == 0:
                    error = "Sıfıra bölme yapılamaz!"
                else:
                    result = number1 / number2
            else:
                error = "Geçersiz işlem!"

        except ValueError:
            error = "Lütfen geçerli sayılar girin!"

    return render_template("index.html", result=result, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
