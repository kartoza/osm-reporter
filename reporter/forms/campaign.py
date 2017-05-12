__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '10/05/17'

from flask_wtf import FlaskForm
from wtforms.fields import DateField, StringField, SubmitField
from wtforms.validators import DataRequired, Optional


class CampaignForm(FlaskForm):
    name = StringField(u'Campaign name', validators=[DataRequired('Campaign name is needed')])
    campaign_status = StringField(u'Campaign status')
    coverage = StringField(u'Coverage')
    start_date = DateField(u'Start date of campaign')
    end_date = DateField(u'End date of campaign', validators=[Optional()])

    submit = SubmitField(u'Create')
