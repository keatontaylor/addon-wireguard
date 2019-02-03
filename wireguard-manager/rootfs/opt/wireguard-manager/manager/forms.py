from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, IPAddress, Length, NumberRange, Regexp, Optional, ValidationError
from manager.models import Interface
from subprocess import run, PIPE, check_output
from ipcalc import Network

class InterfaceForm(FlaskForm):
    interface = IntegerField('Interface Number',
        validators=[DataRequired(), NumberRange(min=1, max=999)])
    port = IntegerField('Port',
        validators=[DataRequired(), NumberRange(min=1, max=65535)])
    address = StringField('IP Address',
        validators=[DataRequired(), IPAddress(ipv4=True, ipv6=True)])
    netmask = IntegerField('Netmask',
        validators=[DataRequired(), NumberRange(min=1, max=128)])
    private_key = StringField('Private Key',
        validators=[Optional(), Length(min=44, max=44)])
    submit = SubmitField('Add Interface')

    def validate_interface(self, interface):
        interface = Interface.query.filter_by(interface=interface.data).first()
        if interface:
            raise ValidationError('That interface number is already being used.')

    def validate_port(self, port):
        interface = Interface.query.filter_by(port=port.data).first()
        p = run(['/opt/port_in_use.sh', 'udp', str(port.data)])
        if p.returncode != 0:
            raise ValidationError('UDP port {str(port.data)} is already in use.')
        if interface:
            raise ValidationError('That port number is already being used.')

    def validate_address(self, address):
        interface = Interface.query.filter_by(address=address.data).first()
        ip_list = check_output(['ip', '-br', 'addr']).decode().splitlines()
        ips = []
        for item in ip_list:
            if len(item) > 2:
                ips.extend(item.split()[2:])
        for ip in ips:
            if Network(f'{ip}').info() == f'LINK-LOCAL':
                if ip == f'{address.data}/{self.netmask.data}':
                    raise ValidationError('{address.data}/{self.netmask.data} is already assigned to another interface.')
            elif Network(f'{address.data}/{self.netmask.data}').check_collision(ip):
                raise ValidationError('{address.data}/{self.netmask.data} is part of a network already assigned to an interface.')
        if interface:
            raise ValidationError('That address is already being used.')

    def validate_private_key(self, private_key):
        interface = Interface.query.filter_by(private_key=private_key.data).first()
        if private_key.data:
            if len(private_key.data) != 44:
                raise ValidationError('The private key must equal 44 characters.')
            p = run(["wg", "pubkey"],
                    stdout=PIPE,
                    stderr=PIPE,
                    input=str.encode(private_key.data))
            if p.returncode != 0:
                raise ValidationError(p.stderr.decode().split(': ')[1].rstrip())
# Remove the following after adding default value to database
#        else:
#            private_key = check_output(['wg', 'genkey']).decode().rstrip()
        if interface:
            raise ValidationError('That private key is already being used.')


class PeerForm(FlaskForm):
    peer = StringField('Peer',
        validators=[DataRequired()])
    public_key = StringField('Public Key',
        validators=[DataRequired(), Length(min=44, max=44)])
    endpoint = StringField('Endpoint',
        validators=[Optional(), Regexp(regex="")])
    allowed_ips = StringField('Allowed IPs',
        validators=[DataRequired(), Regexp(regex="")])
    persistent = IntegerField('Persistent Keepalive',
        validators=[Optional(), NumberRange(min=1, max=30)])
    submit = SubmitField('Add Peer')