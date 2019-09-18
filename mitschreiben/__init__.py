# -*- coding: utf-8 -*-

# mitschreiben
# ------------
# Python library supplying a tool to record values during calculations
# 
# Author:   sonntagsgesicht, based on a fork of Deutsche Postbank [pbrisk]
# Version:  0.3, copyright Wednesday, 18 September 2019
# Website:  https://github.com/sonntagsgesicht/mitschreiben
# License:  Apache License 2.0 (see LICENSE file)


import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())


__doc__ = 'Python library supplying a tool to record values during calculations'
__version__ = '0.3'
__dev_status__ = '4 - Beta'
__date__ = 'Wednesday, 18 September 2019'
__author__ = 'sonntagsgesicht, based on a fork of Deutsche Postbank [pbrisk]'
__email__ = 'sonntagsgesicht@icloud.com'
__url__ = 'https://github.com/sonntagsgesicht/' + __name__
__license__ = 'Apache License 2.0'
__dependencies__ = ('six',)
__dependency_links__ = ()
__data__ = ('html_basics/*',)
__scripts__ = ()


__all__ = ['Record', 'DictTree']

from .recording import Record
from .formatting import DictTree
from .table import Table
