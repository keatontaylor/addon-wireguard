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
        if form.private_key.data:
            # Run `wg pubkey` against private_key entered
            # p = run(['wg', 'genkey'], stdout=PIPE)
            # print(p.stdout.decode().rstrip())

            p = run(["wg", "pubkey"],
                    stdout=PIPE,
                    stderr=PIPE,
                    input=str.encode(form.private_key.data))
            # print(p)
            # CompletedProcess(args=['wg', 'pubkey'], returncode=0, stdout=b'')
            if p.returncode != 0:
                flash(p.stderr.decode().split(': ')[1].rstrip())
                return render_template('interface.html', title='', form=form)
        
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
