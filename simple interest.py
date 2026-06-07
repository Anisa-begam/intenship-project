from flask import Flask, request, jsonify

app = Flask(__name__)

def calculate_simple_interest(principal, rate, time):
    interest = (principal * rate * time) / 100
    total_amount = principal + interest

    return {
        "interest": interest,
        "total_amount": total_amount
    }

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()

    principal = data['principal']
    rate = data['rate']
    time = data['time']

    result = calculate_simple_interest(principal, rate, time)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)