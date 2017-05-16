__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '10/05/17'

from flask_wtf import FlaskForm
from wtforms.fields import DateField, SelectMultipleField, StringField, SubmitField
from wtforms.validators import DataRequired, Optional

from reporter.settings import users
from reporter.models.insights_function import InsightsFunction


class CampaignForm(FlaskForm):
    name = StringField(u'Campaign name', validators=[DataRequired('Campaign name is needed')])
    campaign_status = StringField(u'Campaign status')
    coverage = StringField(u'Coverage')
    start_date = DateField(u'Start date of campaign')
    end_date = DateField(u'End date of campaign', validators=[Optional()])

    campaign_managers = SelectMultipleField(
        u'Managers of campaign', choices=[(user, user) for user in users])
    selected_functions = SelectMultipleField(
        u'Functions for this campaign',
        choices=[
            (insights_function.uuid, insights_function.insight_function)
            for insights_function in InsightsFunction.all()
            ]
    )
    submit = SubmitField(u'Submit')
