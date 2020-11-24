from openerp import fields, models, api


class IncrementConfig(models.Model):
    _name = 'increment.config'
    _description = 'Configures the rates in which salaries get incremented'

    name = fields.Char(required=True)
    increment_config_line_ids = fields.One2many(comodel_name='increment.config.line',
                                                inverse_name='increment_config_reference')

    # maximum_wage = fields.Float(string='Maximum', required=True)
    # maximum_wage_increment = fields.Float(string='Increment amount(%)')


class IncrementConfigLine(models.Model):
    _name = 'increment.config.line'

    increment_config_reference = fields.Many2one(comodel_name='increment.config')

    starting_range = fields.Float(string='Starting Range (Inclusive)')
    ending_range = fields.Float(string='Ending Range')
    salary_increment = fields.Float(string='Increment Amount (%)')
    offset = fields.Float(string='Offset')
