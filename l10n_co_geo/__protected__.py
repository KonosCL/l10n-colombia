# -*- coding: utf-8 -*-
# Copyright 2017, DevCO Colombia
# DevCO Enterprise Edition License v1.0.

from openerp.addons.protector import Protector
from openerp import models


class ResCountryNoEdit(Protector, models.Model):
    _inherit = ['res.country']
    PROTEDTED_FIELDS = ['name', 'code', 'currency_id', 'image', 'phone_code']


class ResCountryStateNoEdit(Protector, models.Model):
    _inherit = ['res.country.state']
    PROTEDTED_FIELDS = ['country_id', 'name', 'code']


class ResCountryStateCityNoEdit(Protector, models.Model):
    _inherit = ['res.country.state.city']
    PROTEDTED_FIELDS = ['name', 'state_id', 'statcode', 'country_id']
