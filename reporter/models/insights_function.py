__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '10/05/17'

import json
import os
from reporter.models.json_model import JsonModel


class InsightsFunction(JsonModel):
    """
    Class insights funtion model that hold campaign information and functions.
    """
    uuid = ''
    insight_function = ''
    ui_template = ''
    summary_template = ''
    detail_template = ''

    def __init__(self, uuid):
        self.uuid = uuid
        self.json_path = InsightsFunction.get_json_file(uuid)
        self.parse_json_file()

    def name(self):
        """ return name of insight function
        """
        return '[%s] %s, %s, %s' % (
            self.insight_function,
            self.ui_template,
            self.summary_template,
            self.detail_template)

    def parse_json_file(self):
        """ Parse json file for this campaign.

        If file is corrupted, it will raise Campaign.CorruptedFile exception.
        """
        if self.json_path:
            try:
                _file = open(self.json_path, 'r')
                content = _file.read()
                content_json = json.loads(content)
                InsightsFunction.validate(content_json, self.uuid)
                attributes = self.get_attributes()
                for key, value in content_json.items():
                    if key in attributes:
                        setattr(self, key, value)
            except json.decoder.JSONDecodeError:
                raise JsonModel.CorruptedFile

    @staticmethod
    def get_json_folder():
        file_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(
            file_path, os.pardir, 'campaigns_data', 'selected_functions')

    @staticmethod
    def serialize(dict):
        """Serialize campaign dictionary

        :key dict: dictionary
        :type dict: dict
        """
        json_str = json.dumps(dict)
        return json_str

    @staticmethod
    def create(dict, uploader):
        """Validate found dict based on campaign class.
        uuid should be same as uuid file.
        """
        dict['version'] = 1
        dict['edited_by'] = uploader

        uuid = dict['uuid']
        InsightsFunction.validate(dict, uuid)

        json_str = InsightsFunction.serialize(dict)
        json_path = os.path.join(
            InsightsFunction.get_json_folder(), '%s.json' % uuid
        )
        _file = open(json_path, 'w+')
        _file.write(json_str)
        _file.close()

    @staticmethod
    def get(uuid):
        """Get insights function from uuid

        :param uuid: UUID of insights function that to be returned
        :type uuid: str

        :return: insights function that found or none
        :rtype: insights function
        """
        return InsightsFunction(uuid)

    @staticmethod
    def all():
        """Get all insights function

        :return: insights function that found or none
        :rtype: [insights function]
        """
        insight_functions = []
        for root, dirs, files in os.walk(InsightsFunction.get_json_folder()):
            for file in files:
                filename = os.path.splitext(file)[0]
                try:
                    insight_functions.append(InsightsFunction(filename))
                except InsightsFunction.DoesNotExist:
                    pass
        return insight_functions

    @staticmethod
    def get_json_file(uuid):
        """ Get path of json file of uuid.
        :param uuid: UUID of json model that to be returned
        :type uuid: str

        :return: path of json or none if not found
        :rtype: str
        """
        json_path = os.path.join(
            InsightsFunction.get_json_folder(), '%s.json' % uuid
        )
        if os.path.isfile(json_path):
            return json_path
        else:
            raise InsightsFunction.DoesNotExist()

    @staticmethod
    def validate(dict, uuid):
        """Validate found dict based on insights function class.
        uuid should be same as uuid file.
        """
        required_attributes = [
            'uuid', 'version', 'edited_by', 'insight_function']
        for required_attribute in required_attributes:
            if required_attribute not in dict:
                raise JsonModel.RequiredAttributeMissed(required_attribute)
            if uuid != dict['uuid']:
                raise Exception('UUID is not same in json.')
        return True

    @staticmethod
    class DoesNotExist(Exception):
        def __init__(self):
            self.message = "insights function doesn't exist"
            super(InsightsFunction.DoesNotExist, self).__init__(self.message)
