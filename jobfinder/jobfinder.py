# -*- coding: utf-8 -*-
# Copyright (C) 2018 William Lake, Greg Beam
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
"""Main Class for finder utility."""

import sys
import os
import logging

from logging.config import fileConfig
from jobfinder import finder
from jobfinder import dbutil


class Driver(object):
    DEFAULT_CONFIG_FILE = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)), 'logging.conf')

    def __init__(self):

        # Always check the DB first before any actions to help prevent errors
        self.checkdb = dbutil.Dbutil.check_db()

        self.load_configuration()

        self.logger = logging.getLogger()

        self.finder = finder.Finder(self.gather_arguments())

        try:

            self.finder.start()

        except Exception as err:

            self.logger.exception(
                'There was an error during finder execution: %r' % err)

        if self.finder.conn_closed == False:
            self.finder.dbutil.close_connection()

    def load_configuration(self, config_file=DEFAULT_CONFIG_FILE):
        """
        Loads logging configuration from the given configuration file.

        Code from: https://github.com/storj/storj-python-sdk/blob/master/tests/log_config.py

        Code found via: https://www.programcreek.com/python/example/105587/logging.config.fileConfig

        :param config_file:
            the configuration file (default=/etc/package/logging.conf)
        :type config_file: str
        """
        if not os.path.exists(config_file) or not os.path.isfile(config_file):
            msg = '%s configuration file does not exist!', config_file

            logging.getLogger().error(msg)

            raise ValueError(msg)

        try:
            fileConfig(config_file, disable_existing_loggers=False)

            logging.getLogger().info('%s configuration file was loaded.',
                                     config_file)

        except Exception as e:

            logging.getLogger().error('Failed to load configuration from %s!',
                                      config_file)

            logging.getLogger().debug(str(e), exc_info=True)

            raise e

    def gather_arguments(self):
        """Gathers the command line arguments if they exist."""

        self.logger.info('Gathering Command Line Arguments')

        args = []

        try:

            args.append(sys.argv[1])

            args.append(sys.argv[2])

            self.logger.debug('Arg 1: {}'.format(args[0]))

            self.logger.debug('Arg 2: {}'.format(args[1]))

        except:

            args = None

            self.logger.debug('Less than 2 arguments provided.')

        return args


def main():
    driver = Driver()


if __name__ == '__main__':
    main()