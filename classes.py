from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Regexp, NumberRange


class ProductForm(FlaskForm):
    customer_id = StringField('Customer ID', [
        DataRequired()])
    product_type = SelectField('Product', [DataRequired()], choices=[('domain', 'Domain'),
                                                              ('hosting', 'Hosting'),
                                                              ('email', 'E-mail'),
                                                              ('pdomain', 'P-Domain'),
                                                              ('edomain', 'E-Domain')])
    domain = StringField('Domain', [DataRequired(), Regexp('(\w+\.\w+)$')])
    duration = IntegerField('Duration', [DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Submit')
