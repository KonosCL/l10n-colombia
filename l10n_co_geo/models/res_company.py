# -*- coding: utf-8 -*-
# Copyright 2016 David Arnold, DevCO Colombia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


class ResCompany(models.Model):
    _name = 'res.company'
    _inherit = ['res.company', 'partner.city.abstract']

    city_id = fields.Many2one(
        'res.country.state.city', 'City',
        compute="_compute_address", inverse='_inverse_city_id')

    @api.onchange('country_id')
    def _onchange_country_wrapper(self):
        values = self.on_change_country(self.country_id.id)['value']
        for fname, value in values.iteritems():
            setattr(self, fname, value)

    # TODO @api.depends(): currently now way to formulate the dependency on the
    # partner's contact address
    def _compute_address(self):
        # TODO BACKPORT
        # refactor if https://github.com/odoo/odoo/pull/15213 gets accepted
        for company in self.filtered(lambda company: company.partner_id):
            address_data = company.partner_id.sudo(
            ).address_get(adr_pref=['contact'])
            if address_data['contact']:
                partner = company.partner_id.browse(address_data['contact'])
                company.city_id = partner.city_id
        return super(ResCompany, self)._compute_address()

    def _inverse_city_id(self):
        for company in self:
            company.partner_id.city_id = company.city_id

    @api.model
    def create(self, vals):
        return super(ResCompany, self).create(self._complete_address(vals))

    @api.multi
    def write(self, vals):
        return super(ResCompany, self).write(self._complete_address(vals))
