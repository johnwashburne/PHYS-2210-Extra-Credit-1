from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/select_units')
def select_units():
    return render_template('selectUnits.html')


@app.route('/convert', methods=['POST'])
def convert():
    if request.method == 'POST':
        unit_dict = json.load(open("units.json", "r"))
        unit_class = request.form.to_dict()['unit']
        units = []
        for key in unit_dict[unit_class]:
            units.append(key)
        return render_template("convert.html", units=units, unit_class=unit_class)
    return 'failed'


@app.route('/results', methods=['POST'])
def results():
    conversions= json.load(open('units.json', 'r'))
    data = request.form.to_dict()
    x = float(data['starting_value'])
    factor = conversions[data['unit_class']][data['starting_unit']]
    intercept1 = 0
    intercept2 = 0
    if isinstance(factor, dict):
        intercept1 = factor['intercept1']
        intercept2 = factor['intercept2']
        factor = factor['factor']
    intermediate = factor * (x - intercept2) + intercept1
    
    factor = conversions[data['unit_class']][data['target_unit']]
    intercept1 = 0
    intercept2 = 0
    if isinstance(factor, dict):
        intercept1 = factor['intercept1']
        intercept2 = factor['intercept2']
        factor = factor['factor']
    final = (intermediate-intercept1) / factor + intercept2
    final = str(round(final, 6))

    return render_template('results.html', final=final, starting_unit=data['starting_unit'].lower(), starting_value=x, target_unit=data['target_unit'].lower())


if __name__ == '__main__':
    app.run()
