from . import db
from subprocess import check_output

def get_private_key():
    return check_output(['wg', 'genkey']).decode().rstrip()

class Interface(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    port = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(), nullable=False)
    netmask = db.Column(db.Integer, nullable=False)
    private_key = db.Column(db.String(44), nullable=False, default=get_private_key)
    enabled = db.Column(db.Boolean, nullable=False, default=False)
    peers = db.relationship('Peer', backref='interface', lazy=True)

    def __repr__(self):
        return f"Interface('wg{self.number}', '{self.address}/{self.netmask}')"


class Peer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    peer = db.Column(db.String(20), unique=True, nullable=False)
    public_key = db.Column(db.String(44), nullable=False)
    endpoint = db.Column(db.String())
    allowed_ips = db.Column(db.String())
    persistent = db.Column(db.Integer)
    enabled = db.Column(db.Boolean, nullable=False, default=False)
    interface_id = db.Column(db.Integer, db.ForeignKey('interface.id'), nullable=False)

    def __repr__(self):
        return f"Peer('{self.peer}', '{self.endpoint}/{self.allowed_ips}')"
