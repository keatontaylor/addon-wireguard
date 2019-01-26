from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import InterfaceForm, PeerForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '6a598f99f0915fd9f158ae5597aad87d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////data/wg.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Interface(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    interface = db.Column(db.Integer, unique=True, nullable=False)
    port = db.Column(db.Integer, unique=True, nullable=False)
    address = db.Column(db.String(), unique=True, nullable=False)
    subnet_mask = db.Column(db.Integer, nullable=False)
    private_key = db.Column(db.String(44), unique=True, nullable=False)
    peers = db.relationship('Peer', backref='interface', lazy=True)

    def __repr__(self):
        return f"Interface('wg{self.interface}', '{self.address}/{self.subnet_mask}')"


class Peer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    peer = db.Column(db.String(20), unique=True, nullable=False)
    public_key = db.Column(db.String(44), nullable=False)
    endpoint = db.Column(db.String())
    allowed_ips = db.Column(db.String())
    persistent = db.Column(db.Integer)
    interface_id = db.Column(db.Integer, db.ForeignKey('integer.id'), nullable=False)

    def __repr__(self):
        return f"Peer('{self.peer}', '{self.endpoint}/{self.allowed_ips}')"


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