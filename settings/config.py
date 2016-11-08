import ConfigParser
import logging
import os
import sys

logging.basicConfig()
logger = logging.getLogger("aws.config")
logger.setLevel(logging.INFO)


class Config(object):
    def __init__(self, configfile=None):
        if configfile is None:
            self.configfile = os.path.join(os.path.dirname(__file__),
                                           '..',
                                           'aws.config')
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.configfile)

        try:
            self.AWS_KEY = self.config.get('AWS keys', \
                                                'AWS_KEY')
            self.AWS_SECRET = self.config.get('AWS keys', \
                                                   'AWS_SECRET')
        except ConfigParser.NoSectionError as e:
                logger.warn(e)
                sys.exit(1)
