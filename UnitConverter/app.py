from flask import Flask, render_template, request, jsonify # type: ignore

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    value = float(data['value'])
    category = data['category']
    from_unit = data['from']
    to_unit = data['to']

    result = value

    # LENGTH (convert everything to meters first)
    if category == "length":
        length_to_m = {
            "km": 1000,
            "m": 1,
            "cm": 0.01,
            "mm": 0.001,
            "foot": 0.3048,
            "inch": 0.0254
        }
        result = value * length_to_m[from_unit] / length_to_m[to_unit]

    # WEIGHT (convert everything to grams first)
    elif category == "weight":
        weight_to_g = {
            "kg": 1000,
            "gm": 1,
            "pound": 453.592
        }
        result = value * weight_to_g[from_unit] / weight_to_g[to_unit]

    # TEMPERATURE (special formulas)
    elif category == "temperature":
        # Convert to Celsius first
        if from_unit == "fahrenheit":
            value = (value - 32) * 5/9
        elif from_unit == "kelvin":
            value = value - 273.15

        # Convert from Celsius to target
        if to_unit == "fahrenheit":
            result = (value * 9/5) + 32
        elif to_unit == "kelvin":
            result = value + 273.15
        else:
            result = value

    return jsonify({"result": round(result, 4)})

if __name__ == '__main__':
    app.run(debug=True)