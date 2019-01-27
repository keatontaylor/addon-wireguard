from manager import db

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
    interface_id = db.Column(db.Integer, db.ForeignKey('interface.id'), nullable=False)

    def __repr__(self):
        return f"Peer('{self.peer}', '{self.endpoint}/{self.allowed_ips}')"
