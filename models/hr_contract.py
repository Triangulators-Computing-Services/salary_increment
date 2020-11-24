# -*- coding: utf-8 -*-

from openerp import fields, models, api


class HrEmployee(models.Model):
    _inherit = 'hr.contract'

    #efficiency_input_reference = fields.Many2one('efficiency.input')
