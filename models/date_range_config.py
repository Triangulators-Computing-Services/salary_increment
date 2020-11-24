from openerp import fields, models, api


class DateRangeConfig(models.Model):
    _name = 'dateRange.config'
    _description = 'Configures the time periods in which evaluation is made'

    name = fields.Char(required=True)
    dateRange_config_line_ids = fields.One2many(comodel_name='dateRange.config.line',
                                                inverse_name='dateRange_config_reference')

    # @api.model
    # def create(self, vals):
    #


class dateRangeConfigLine(models.Model):
    _name = 'dateRange.config.line'

    dateRange_config_reference = fields.Many2one(comodel_name='dateRange.config')

    starting_range = fields.Float(string='Starting Range')
    ending_range = fields.Float(string='Ending Range')
    salary_increment = fields.Float(string='Increment Amount')
