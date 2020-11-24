from openerp import fields, models, api


class SalaryConfig (models.Model):
    _name = 'salary.config'

    name = fields.Char(required=True)
    salary_config_line_ids = fields.One2many(comodel_name='salary.config.line', inverse_name='salary_config_reference')

class SalaryConfigLine (models.Model):
    _name ='salary.config.line'

    salary_config_reference = fields.Many2one(comodel_name='salary.config')

    starting_range = fields.Float(string='Starting Range')
    ending_range = fields.Float(string='Ending Range')
    salary_increment = fields.Float(string='Increment Amount')



