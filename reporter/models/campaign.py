__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '10/05/17'

import datetime
import json
import os
from reporter.models.version import Version

file_path = os.path.dirname(os.path.abspath(__file__))
campaign_path = os.path.join(file_path, os.pardir, 'campaigns_data', 'campaign')


class Campaign(Version):
    """
    Class campaign model that hold campaign information and functions.
    """
    required = 'uuid'
    uuid = ''
    name = ''
    campaign_creator = ''
    campaign_status = ''
    coverage = ''
    geometry = None
    start_date = None
    end_date = None
    campaign_managers = []
    selected_function = []

    json_path = ''

    def __init__(self, uuid):
        self.uuid = uuid
        self.json_path = Campaign.get_json_file(uuid)
        self.parse_json_file()

    def parse_json_file(self):
        """ Parse json file for this campaign.

        If file is corrupted, it will raise Campaign.CorruptedFile exception.
        """
        if self.json_path:
            try:
                _file = open(self.json_path, 'r')
                content = _file.read()
                content_json = json.loads(content)
                Campaign.validate(content_json, self.uuid)
                attributes = self.get_attributes()
                for key, value in content_json.items():
                    if key in attributes:
                        setattr(self, key, value)
            except json.decoder.JSONDecodeError:
                raise Campaign.CorruptedFile

    def update_data(self, dict, uploader):
        """ Update data with new dict.
        """
        for key, value in dict.items():
            setattr(self, key, value)
        self.version += 1
        self.edited_by = uploader

        # save updated campaign to json
        dict = self.to_dict()
        Campaign.validate(dict, self.uuid)
        json_str = Campaign.serialize(dict)
        json_path = os.path.join(
            campaign_path, '%s.json' % self.uuid
        )
        _file = open(json_path, 'w+')
        _file.write(json_str)
        _file.close()

    def get_attributes(self):
        """ Get attributes of campaign
        :return: attributes
        :rtype: list
        """
        return [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]

    def to_dict(self):
        """ Return campaign model as dictionary.
        :return: dict
        """
        dict = {}
        for attribute in self.get_attributes():
            dict[attribute] = getattr(self, attribute)
        return dict

    @staticmethod
    def serialize(dict):
        """Serialize campaign dictionary

        :key dict: dictionary
        :type dict: dict
        """
        dict['start_date'] = dict['start_date'].strftime('%Y-%m-%d')
        if dict['end_date']:
            dict['end_date'] = dict['end_date'].strftime('%Y-%m-%d')
        json_str = json.dumps(dict)
        return json_str

    @staticmethod
    def create(dict, uploader):
        """Validate found dict based on campaign class.
        uuid should be same as uuid file.
        """
        dict['version'] = 1
        dict['edited_by'] = uploader
        dict['campaign_creator'] = uploader

        uuid = dict['uuid']
        Campaign.validate(dict, uuid)

        json_str = Campaign.serialize(dict)
        json_path = os.path.join(
            campaign_path, '%s.json' % uuid
        )
        _file = open(json_path, 'w+')
        _file.write(json_str)
        _file.close()

    @staticmethod
    def get_json_file(uuid):
        """ Get path of json file of uuid.
        :param uuid: UUID of campaign that to be returned
        :type uuid: str

        :return: path of json or none if not found
        :rtype: str
        """
        json_path = os.path.join(
            campaign_path, '%s.json' % uuid
        )
        if os.path.isfile(json_path):
            return json_path
        else:
            raise Campaign.DoesNotExist()

    @staticmethod
    def get(uuid):
        """Get campaign from uuid

        :param uuid: UUID of campaign that to be returned
        :type uuid: str

        :return: Campaign that found or none
        :rtype: Campaign
        """
        return Campaign(uuid)

    @staticmethod
    def validate(dict, uuid):
        """Validate found dict based on campaign class.
        uuid should be same as uuid file.
        """
        required_attributes = ['uuid', 'version', 'campaign_creator', 'edited_by', 'name']
        for required_attribute in required_attributes:
            if required_attribute not in dict:
                raise Campaign.RequiredAttributeMissed(required_attribute)
            if uuid != dict['uuid']:
                raise Exception('UUID is not same in json.')
        return True

    @staticmethod
    class RequiredAttributeMissed(Exception):
        def __init__(self, attribute):
            self.message = "%s is missed" % attribute
            super(Campaign.RequiredAttributeMissed, self).__init__(self.message)

    @staticmethod
    class CorruptedFile(Exception):
        def __init__(self):
            self.message = "Json file for this campaign is corrupted"
            super(Campaign.CorruptedFile, self).__init__(self.message)

    @staticmethod
    class DoesNotExist(Exception):
        def __init__(self):
            self.message = "Campaign doesn't exist"
            super(Campaign.DoesNotExist, self).__init__(self.message)
