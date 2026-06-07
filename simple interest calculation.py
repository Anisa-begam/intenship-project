# Simple Interest Calculator API

from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('simple_interest.html')

@app.route('/simple-interest-calculator', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        principal = float(data['principal'])
        rate = float(data['rate'])
        time = float(data['time'])
        
        simple_interest = (principal * rate * time) / 100
        total_amount = principal + simple_interest
        
        return jsonify({
            'simple_interest': simple_interest,
            'total_amount': total_amount
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)