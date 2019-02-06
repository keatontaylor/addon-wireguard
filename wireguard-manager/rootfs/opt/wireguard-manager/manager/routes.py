from flask import render_template, url_for, flash, redirect
from manager import app, db
from manager.forms import InterfaceForm, PeerForm
from manager.models import Interface, Peer

@app.route('/')
def home():
    interfaces = Interface.query.all()
    return render_template('home.html', interfaces=interfaces)

@app.route('/interface', methods=['GET', 'POST'])
def interface():
    form = InterfaceForm()
    if form.validate_on_submit():
        interface = Interface(number=form.number.data,
                                port=form.port.data,
                                address=form.address.data,
                                netmask=form.netmask.data,
                                private_key=form.private_key.data)
        db.session.add(interface)
        db.session.commit()
        flash('You have submitted a valid form!', 'success')
        return redirect(url_for('home'))
    return render_template('interface.html', title='', form=form)

@app.route('/peer', methods=['GET', 'POST'])
def peer():
    form = PeerForm()
    if form.validate_on_submit():
        flash('You have submitted a valid form!', 'success')
        return redirect(url_for('home'))
    return render_template('peer.html', title='', form=form)
