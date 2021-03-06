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
""" Database COnnection

    Represents the connection to the database, centralizing transactions
    and management.
"""
import logging
import sqlite3

from jobfinder import dbutil

class Dbconnection(object):

    def __init__(self):
        """Constructor"""
   
        self.logger = logging.getLogger()
        self.logger.info(dbutil.Dbutil.check_db())
        self.logger.info('Connecting To DB')
        self.conn = sqlite3.connect(dbutil.Dbutil.get_db_path())

    def execute_insert(self, statement, params=None):
        """Executes an INSERT on the database.
        
        Arguments:
            statement {str} -- The SQL statement to execute.
        
        Keyword Arguments:
            params {list} -- The parameters to use when executing the SQL
            statement. (default: {None})
        """

        self.execute_statement(statement, params)

    def execute_select(self, statement, params=None):
        """Executes a SELECT statement on the database, returning the results.
        
        Arguments:
            statement {str} -- The SQL statement to execute.
        
        Keyword Arguments:
            params {list} -- The parameters to use when executing the
            SQL statement. (default: {None})
        
        Returns:
            list -- The results of the given SQL SELECT statement.
        """

        if params is None:
            results = self.conn.execute(statement)

        else:
            results = self.conn.execute(statement, params)

        return results

    def execute_update(self, statement, params=None):
        """Executes an UPDATE statement on the database.
        
        Arguments:
            statement {str} -- The SQL statement to execute.
        
        Keyword Arguments:
            params {list} -- The parameters to use when executing the SQL
            statement. (default: {None})
        """

        self.execute_statement(statement, params)

    def execute_delete(self, statement, params=None):
        """Executes a DELETE statement on the database.
        
        Arguments:
            statement {str} -- The SQL statement to execute.
        
        Keyword Arguments:
            params {list} -- The parameters to use when executing the SQL
            statement. (default: {None})
        """

        self.execute_statement(statement, params)

    def execute_statement(self, statement, params=None):
        """Executes the given statement on the database.
        
        Arguments:
            statement {str} -- The SQL statement to execute.
        
        Keyword Arguments:
            params {list} -- The parameters to use when executing the SQL
            statement.. (default: {None})
        """
        if params is None:
            self.conn.execute(statement)
        else:
            self.conn.execute(statement, params)

        self.conn.commit()

    def close(self):
        """Closes the database connection, commiting the changes if necessary.
        
        Keyword Arguments:
            do_commit {boolean} -- True if the database changes should be
            committed. (default: {False})
        """
        self.logger.info = 'Closing db'
        self.conn.commit()
        self.conn.close()
