# Salary Tax Calculator API

from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('salary_tax.html')

@app.route('/calculate-salary', methods=['POST'])
def calculate_salary():
    try:
        data = request.get_json()
        base_salary = float(data['base_salary'])
        hours_worked = float(data['hours_worked'])
        hourly_rate = float(data['hourly_rate'])
        
        gross_salary = base_salary + (hours_worked * hourly_rate)
        
        return jsonify({
            'gross_salary': gross_salary
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/calculate-tax', methods=['POST'])
def calculate_tax():
    try:
        data = request.get_json()
        salary = float(data['salary'])
        tax_rate = float(data['tax_rate'])
        
        tax_amount = (salary * tax_rate) / 100
        net_salary = salary - tax_amount
        
        return jsonify({
            'tax_amount': tax_amount,
            'net_salary': net_salary
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/calculate-salary-tax', methods=['POST'])
def calculate_salary_tax():
    try:
        data = request.get_json()
        base_salary = float(data['base_salary'])
        hours_worked = float(data['hours_worked'])
        hourly_rate = float(data['hourly_rate'])
        tax_rate = float(data['tax_rate'])
        
        gross_salary = base_salary + (hours_worked * hourly_rate)
        tax_amount = (gross_salary * tax_rate) / 100
        net_salary = gross_salary - tax_amount
        
        return jsonify({
            'base_salary': base_salary,
            'hours_worked': hours_worked,
            'hourly_rate': hourly_rate,
            'gross_salary': gross_salary,
            'tax_rate': tax_rate,
            'tax_amount': tax_amount,
            'net_salary': net_salary
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)