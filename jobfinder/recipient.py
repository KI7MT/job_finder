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
"""
Recipient

Represents a recipient of new job notifications.
"""


class Recipient(object):

    def __init__(self, recipient_id, email, date_added):
        """Constructor
        
        Arguments:
            recipient_data {list} -- The data to use when building this recipient object.
        """

        self.recipient_id = recipient_id

        self.email = email

        self.date_added = date_added
