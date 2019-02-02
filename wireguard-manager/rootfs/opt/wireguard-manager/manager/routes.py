from flask import render_template, url_for, flash, redirect
from manager import app
from manager.forms import InterfaceForm, PeerForm
from manager.models import Interface, Peer
from subprocess import run, PIPE

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/interface', methods=['GET', 'POST'])
def interface():
    form = InterfaceForm()
    if form.validate_on_submit():
        failed = False
        # Check if port is in use
        p = run(['/opt/port_in_use.sh', 'udp', form.port.data.str])
        if p.returncode != 0:
            flash(f'UDP port {form.port.data.str} is already in use.')
            failed = True
        
        # Check if IP address exists on any other interface

        # Check if private_key is valid WireGuard key
        if form.private_key.data:
            p = run(["wg", "pubkey"],
                    stdout=PIPE,
                    stderr=PIPE,
                    input=str.encode(form.private_key.data))
            if p.returncode != 0:
                flash(p.stderr.decode().split(': ')[1].rstrip())
                failed = True
        
        if not failed:
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
