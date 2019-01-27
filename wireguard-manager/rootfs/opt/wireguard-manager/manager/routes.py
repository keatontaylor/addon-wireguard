from flask import render_template, url_for, flash, redirect
from manager import app
from manager.forms import InterfaceForm, PeerForm
from manager.models import Interface, Peer

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
