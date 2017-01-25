# -*- coding: utf-8 -*-
# Copyright 2016 David Arnold, DevCO Colombia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from . import models
try:
    import __protected__
except:
    import logging
    _logger = logging.getLogger(__name__)
    _logger.warning('Not protected.')
