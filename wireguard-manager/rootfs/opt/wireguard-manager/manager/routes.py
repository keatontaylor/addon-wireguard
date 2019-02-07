from flask import render_template, url_for, flash, redirect, request
from . import app, db
from .forms import InterfaceForm, PeerForm
from .models import Interface, Peer

@app.route('/')
def home():
    interfaces = Interface.query.all()
    return render_template('home.html', interfaces=interfaces)

@app.route('/interface/new', methods=['GET', 'POST'])
def interface_new():
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
    return render_template('interface_form.html', title='', form=form)

@app.route('/interface/<int:id>/edit', methods=['GET', 'POST'])
def interface_edit(id):
    interface = Interface.query.get_or_404(id)
    form = InterfaceForm()
    if form.validate_on_submit():
        interface.number=form.number.data
        interface.port=form.port.data
        interface.address=form.address.data
        interface.netmask=form.netmask.data
        interface.private_key=form.private_key.data
        db.session.commit()
        flash('You have updated the interface!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.number.data = interface.number
        form.port.data = interface.port
        form.address.data = interface.address
        form.netmask.data = interface.netmask
        form.private_key.data = interface.private_key
    return render_template('interface_form.html', title='', form=form)

@app.route('/interface/<int:id>')
def interface(id):
    interface = Interface.query.get_or_404(id)
    return render_template('interface.html', title='', interface=interface)

@app.route('/interface/<int:id>/delete', methods=['GET', 'POST'])
def interface_delete(id):
    interface = Interface.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(interface)
        db.session.commit()
        flash('The interface has been deleted.', 'success')
        return redirect(url_for('home'))
    return render_template('interface_delete.html', title='', interface=interface)

@app.route('/peer', methods=['GET', 'POST'])
def peer():
    form = PeerForm()
    if form.validate_on_submit():
        flash('You have submitted a valid form!', 'success')
        return redirect(url_for('home'))
    return render_template('peer.html', title='', form=form)
