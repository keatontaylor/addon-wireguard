from flask import Flask, render_template, url_for
from forms import InterfaceForm, PeerForm

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/interface')
def interface():
    form = InterfaceForm()
    return render_template('interface.html', title='', form=form)

@app.route('/peer')
def peer():
    form = PeerForm()
    return render_template('peer.html', title='', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="%%PORT%%", debug=True)