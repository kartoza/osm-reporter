__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '17/05/17'

from abc import ABCMeta
from flask import render_template


class AbstractInsightsFunction(object):
    """
    Abstract class insights function.
    """
    __metaclass__ = ABCMeta
    function_data = None

    def __init__(self, campaign):
        self.campaign = campaign

    def get_ui_html_file(self):
        """ Get ui name in templates
        :return: string name of html
        :rtype: str
        """
        raise NotImplementedError()

    def get_summary_html_file(self):
        """ Get summary name in templates
        :return: string name of html
        :rtype: str
        """
        raise NotImplementedError()

    def get_details_html_file(self):
        """ Get summary name in templates
        :return: string name of html
        :rtype: str
        """
        raise NotImplementedError()

    def get_required_attributes(self):
        """ Get required attributes for function provider.
        :return: list of required attributes
        :rtype: [str]
        """
        raise NotImplementedError()

    def process_data(self, raw_data):
        """ Get geometry of campaign.
        :param raw_data: Raw data that returns by function provider
        :type raw_data: dict

        :return: processed data
        :rtype: dict
        """
        raise NotImplementedError()

    def run(self):
        """Process this function"""
        raw_data = self._call_function_provider()
        self.function_data = self.process_data(raw_data)

    def _get_geometry(self):
        """ Get geometry of campaign.
        :return: geometry
        :rtype: [str]
        """
        return self.campaign.geometry

    def _call_function_provider(self):
        """ Get required attrbiutes for function provider.
        :return: list of required attributes
        :rtype: [str]
        """
        geometry = self._get_geometry()
        # ---------------------------------
        # here calls function provider
        # ---------------------------------
        return {}

    def _get_html(self, html_name):
        """preprocess for get html function
        :param html_name: html name that need to be processed
        :type html_name: str

        :return: clean html name
        :rtype: str
        """
        if not self.function_data:
            self._call_function_provider()
        return html_name.replace('.html')

    def get_ui_html(self):
        """Return ui in html format"""
        html_file = self._get_html(self.get_ui_html_file())
        return render_template(
            'campaign_widget/ui/%s.html' % html_file, **self.function_data)

    def get_summary_html(self):
        """Return summary in html format"""
        html_file = self._get_html(self.get_summary_html_file())
        return render_template(
            'campaign_widget/summary/%s.html' % html_file, **self.function_data)

    def get_details_html(self):
        """Return details in html format"""
        html_file = self._get_html(self.get_details_html_file())
        return render_template(
            'campaign_widget/details/%s.html' % html_file, **self.function_data)
