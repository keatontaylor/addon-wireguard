from flask import render_template, url_for, flash, redirect
from manager import app
from manager.forms import InterfaceForm, PeerForm
from manager.models import Interface, Peer
from subprocess import run, PIPE, check_output
from ipcalc import Network

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/interface', methods=['GET', 'POST'])
def interface():
    form = InterfaceForm()
    if form.validate_on_submit():
        failed = False
        # Check if port is in use
        p = run(['/opt/port_in_use.sh', 'udp', str(form.port.data)])
        if p.returncode != 0:
            flash(f'UDP port {str(form.port.data)} is already in use.')
            failed = True

        # Check if IP address exists on any other interface
        ip_list = check_output(['ip', '-br', 'addr']).decode().splitlines()
        ips = []
        for item in ip_list:
            if len(item) > 2:
                ips.append(item.split()[2:])
        for ip in ips:
            if Network(f'{ip}').info() == f'LINK-LOCAL':
                if ip == f'{form.address.data}/{form.subnet_mask.data}':
                    flash(f'{form.address.data}/{form.subnet_mask.data} is already assigned to another interface.')
                    failed = True
            elif Network(f'{form.address.data}/{form.subnet_mask.data}').check_collision(ip):
                flash(f'{form.address.data}/{form.subnet_mask.data} is part of a network already assigned to an interface.')
                failed = True

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
