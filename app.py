
from flask import Flask, request, jsonify

app = Flask(__name__)

members = []


@app.route("/")
def home():
    return jsonify({
        "application": "ACEest Fitness & Gym",
        "version": "1.0",
        "status": "Running"
    })


@app.route("/register", methods=["POST"])
def register_member():
    data = request.get_json(silent=True) or {}

    name = data.get("name")
    age = data.get("age")

    if not name or not age:
        return jsonify({"error": "Name and age are required"}), 400

    try:
        age = int(age)
    except (ValueError, TypeError):
        return jsonify({"error": "Age must be a number"}), 400

    if age <= 0:
        return jsonify({"error": "Age must be positive"}), 400

    member = {
        "id": len(members) + 1,
        "name": name,
        "age": age
    }

    members.append(member)

    return jsonify({
        "message": "Member registered successfully",
        "member": member
    }), 201


@app.route("/members")
def get_members():
    return jsonify(members)


@app.route("/bmi", methods=["POST"])
def calculate_bmi():
    data = request.get_json(silent=True) or {}

    try:
        weight = float(data.get("weight", 0))
        height = float(data.get("height", 0))
    except (ValueError, TypeError):
        return jsonify({"error": "Weight and height must be numbers"}), 400

    if weight <= 0 or height <= 0:
        return jsonify({"error": "Weight and height must be positive"}), 400

    bmi = round(weight / (height ** 2), 2)

    return jsonify({
        "bmi": bmi,
        "category": (
            "Underweight" if bmi < 18.5 else
            "Normal" if bmi < 25 else
            "Overweight" if bmi < 30 else
            "Obese"
        )
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

