from flask import Flask, render_template, url_for, flash, redirect
from forms import InterfaceForm, PeerForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '6a598f99f0915fd9f158ae5597aad87d'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/interface', methods=['GET', 'POST'])
def interface():
    form = InterfaceForm()
    if form.validate_on_submit():
        flash(f'You have submitted a valid form!', 'success')
        return redirect(url_for('home'))
    return render_template('interface.html', title='', form=form)

@app.route('/peer', methods=['GET', 'POST'])
def peer():
    form = PeerForm()
    if form.validate_on_submit():
        flash(f'You have submitted a valid form!', 'success')
        return redirect(url_for('home'))
    return render_template('peer.html', title='', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="%%PORT%%", debug=True)