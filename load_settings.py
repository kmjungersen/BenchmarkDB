"""

"""

from ConfigParser import RawConfigParser


class LocalSettings():
    """

    """

    def __init__(self, config_file='znc_settings.conf'):

        settings = self.load_settings(config_file)

        self.mongo_ip = settings['mongo_ip']
        self.mongo_port = settings['mongo_port']

    @staticmethod
    def load_settings(config_file_path):
        """ This function creates the RawConfigParser object that parses
        settings from the config file.  It then takes those settings and
        creates a dict of the options which can then be made into attributes.

        :param config_file_path: the file path of the config file

        :return config_settings: a dict with all parsed settings from the file

        """

        config_settings = {}

        config = RawConfigParser()
        config.read(config_file_path)

        section_list = [
            'MONGO_CONFIG',
        ]

        for section in section_list:

            options_list = config.options(section)

            for option in options_list:

                config_settings[option] = config.get(section, option)

        return config_settings

