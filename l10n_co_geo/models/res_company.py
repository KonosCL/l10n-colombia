# -*- coding: utf-8 -*-
# Copyright 2016 David Arnold, DevCO Colombia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import models, fields, api


class ResCompany(models.Model):
    _name = 'res.company'
    _inherit = ['res.company', 'partner.city.abstract']

    # Backport of v10
    street = fields.Char(compute='_compute_address', inverse='_inverse_street')
    street2 = fields.Char(compute='_compute_address',
                          inverse='_inverse_street2')
    zip = fields.Char(compute='_compute_address', inverse='_inverse_zip')
    city = fields.Char(compute='_compute_address', inverse='_inverse_city')
    state_id = fields.Many2one('res.country.state', compute='_compute_address',
                               inverse='_inverse_state', string="Fed. State")
    country_id = fields.Many2one(
        'res.country', compute='_compute_address',
        inverse='_inverse_country', string="Country")
    fax = fields.Char(compute='_compute_address', inverse='_inverse_fax')
    city_id = fields.Many2one(
        'res.country.state.city', 'City',
        compute="_compute_address", inverse='_inverse_city_id', store=False)

    @api.onchange('country_id')
    def _onchange_country_wrapper(self):
        values = self.on_change_country(self.country_id.id)['value']
        for fname, value in values.iteritems():
            setattr(self, fname, value)

    # TODO @api.depends(): currently now way to formulate the dependency on the
    # partner's contact address
    def _compute_address(self):
        for company in self.filtered(lambda company: company.partner_id):
            address_data = company.partner_id.sudo(
            ).address_get(adr_pref=['contact'])
            if address_data['contact']:
                partner = company.partner_id.browse(address_data['contact'])
                company.street = partner.street
                company.street2 = partner.street2
                company.city = partner.city
                company.zip = partner.zip
                company.state_id = partner.state_id
                company.city_id = partner.city_id
                company.country_id = partner.country_id
                company.fax = partner.fax

    def _inverse_street(self):
        for company in self:
            company.partner_id.street = company.street

    def _inverse_street2(self):
        for company in self:
            company.partner_id.street2 = company.street2

    def _inverse_zip(self):
        for company in self:
            company.partner_id.zip = company.zip

    def _inverse_city(self):
        for company in self:
            company.partner_id.city = company.city

    def _inverse_city_id(self):
        for company in self:
            company.partner_id.city_id = company.city_id

    def _inverse_state(self):
        for company in self:
            company.partner_id.state_id = company.state_id

    def _inverse_country(self):
        for company in self:
            company.partner_id.country_id = company.country_id

    def _inverse_fax(self):
        for company in self:
            company.partner_id.fax = company.fax

    @api.model
    def create(self, vals):
        return super(ResCompany, self).create(self._complete_address(vals))

    @api.multi
    def write(self, vals):
        return super(ResCompany, self).write(self._complete_address(vals))
