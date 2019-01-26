from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, IPAddress, Length, NumberRange, Regexp

class InterfaceForm(FlaskForm):
    interface = IntegerField('Interface Number',
        validators=[DataRequired(), NumberRange(min=1, max=999)])
    port = IntegerField('Port',
        validators=[DataRequired(), NumberRange(min=1, max=65535)])
    address = StringField('IP Address',
        validators=[DataRequired(), IPAddress(ipv4=True, ipv6=True)])
    subnet_mask = IntegerField('Subnet Mask',
        validators=[DataRequired(), NumberRange(min=1, max=32)])
    private_key = StringField('Private Key',
        validators=[Length(min=44, max=44)])
    submit = SubmitField('Add Interface')

class PeerForm(FlaskForm):
    peer = StringField('Peer',
        validators=[DataRequired()])
    public_key = StringField('Public Key',
        validators=[DataRequired(), Length(min=44, max=44)])
    endpoint = StringField('Endpoint',
        validators=[Regexp(regex="")])
    allowed_ips = StringField('Allowed IPs',
        validators=[Regexp(regex="")])
    persistent = IntegerField('Persistent Keepalive',
        validators=[NumberRange(min=1, max=30)])
    submit = SubmitField('Add Peer')