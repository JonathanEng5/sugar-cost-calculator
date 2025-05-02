from flask import Flask, render_template, request
app = Flask(__name__)

# Constants
SUGAR_PER_CAN_GRAMS = 39  # average sugar per 12 oz can
GRAMS_TO_KG = 0.001
COST_PER_DIABETES_CASE = 15000  # USD annual estimated cost
DIABETES_BASELINE_RISK = 0.1  # baseline 10% chance

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    cans_per_year = int(request.form['cans'])
    total_sugar_kg = cans_per_year * SUGAR_PER_CAN_GRAMS * GRAMS_TO_KG

    # Simple risk model
    risk_multiplier = min(total_sugar_kg / 10, 2.0)  # cap the multiplier
    diabetes_risk = round(DIABETES_BASELINE_RISK * risk_multiplier, 2)

    # Simple cost model
    expected_cost = round(diabetes_risk * COST_PER_DIABETES_CASE, 2)

    return render_template('result.html', sugar=round(total_sugar_kg, 2),
                           risk=diabetes_risk, cost=expected_cost)
