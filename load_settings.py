"""

"""

from ConfigParser import RawConfigParser


class LocalSettings():
    """

    """

    def __init__(self, config_file='db_settings.conf'):

        settings = self.load_settings(config_file)

        self.vagrant_1 = settings['vagrant_1']
        self.vagrant_2 = settings['vagrant_2']
        self.vagrant_3 = settings['vagrant_3']
        self.vagrant_4 = settings['vagrant_4']

        self.mongo_port = int(settings['mongo_port'])
        self.riak_port = int(settings['riak_port'])

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
            'MONGO CONFIG',
        ]

        for section in section_list:

            options_list = config.options(section)

            for option in options_list:

                config_settings[option] = config.get(section, option)

        return config_settings

if __name__ == '__main__':
    LocalSettings()