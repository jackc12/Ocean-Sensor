from wtforms import Form, BooleanField, DecimalField, PasswordField, validators

data_dict = {
    'conductivity': {
        'calibrate': False,
        'interval': 0,
        'n_samples': 0
    },
    'oxygen': {
        'calibrate': False,
        'interval': 0,
        'n_samples': 0
    }
}

max_cond_interval, max_cond_n_samples, max_oxygen_interval, max_oxygen_n_samples = 2000, 3000, 3000, 8000

class RegistrationForm(Form):
    conductivity_interval = DecimalField(label='Sample Interval (should be an integer):', validators=[validators.NumberRange(min=0, max=max_cond_interval, message='between 0 and {}'.format(max_cond_interval))])
    conductivity_n_samples = DecimalField(label='Number of Samples (should be an integer):', validators=[validators.NumberRange(min=0, max=max_cond_n_samples, message='between 0 and {}'.format(max_cond_n_samples))])
    oxygen_interval = DecimalField(label='Sample Interval (should be an integer):', validators=[validators.NumberRange(min=0, max=max_oxygen_interval, message='between 0 and {}'.format(max_oxygen_interval))])
    oxygen_n_samples = DecimalField(label='Number of Samples (should be an integer):', validators=[validators.NumberRange(min=0, max=max_oxygen_n_samples, message='between 0 and {}'.format(max_oxygen_n_samples))])


from flask import Flask, request, render_template, redirect
app = Flask(__name__)

@app.route('/conductivity_calibrated')
def conductivity_calibrated():
    data_dict['conductivity']['calibrate'] = True
    return redirect('/')

@app.route('/oxygen_calibrated')
def oxygen_calibrated():
    data_dict['oxygen']['calibrate'] = True
    return redirect('/')


@app.route('/', methods=['GET', 'POST'])
def pilog2020():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        data_dict['conductivity']['interval'] = float(form.conductivity_interval.data)
        data_dict['conductivity']['n_samples'] = float(form.conductivity_n_samples.data)
        data_dict['oxygen']['interval'] = float(form.oxygen_interval.data)
        data_dict['oxygen']['n_samples'] = float(form.oxygen_n_samples.data)

    return render_template('pilog2020.html', form=form)


@app.route('/data', methods=['GET'])
def get_data():
    return data_dict


@app.route('/data/<sensor>', methods=['GET', 'PUT'])
def post_data(sensor):
    if request.method == 'PUT':
        data_dict[sensor]['calibrate'] = False if request.form['calibrate'] else True
    return data_dict[sensor]


if __name__ == "__main__":
    app.run(debug=True)
