# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import Warning
from openerp import exceptions
from datetime import datetime


class EfficiencyInput(models.Model):
    _name = 'efficiency.input'
    _inherit = ["mail.thread", "ir.needaction_mixin"]

    name = fields.Char(readonly=True)
    department = fields.Many2one('hr.department', string='Department', required=True)

    current_date = fields.Date.today()

    increment_year = fields.Char(string='Increment Year', readonly=True, invisible=True)
    use_x_percent_benefit = fields.Boolean(string='Use 5 Year Benefit')

    employee_ids = fields.One2many(comodel_name='employees.list', inverse_name='efficiency_input_id',
                                   help='List of employees in the selected department up for increment\n\n '
                                        'Deduct = Expected Increment - Actual Increment\n'
                                        'Punishment Return: Amount from which the employee lost last year as deduct\n'
                                        '2% Benefit: Amount issued to employees whi have served more than 5 years\n'
                                        'Award: Amount issued to an employee by the company')

    increment_config = fields.Many2one('increment.config', string='Salary Increment Configuration', required=True)

    remark = fields.Text(strint="Remark")

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("input", "Input"),
            ("awaiting_approval", "Awaiting Approval"),
            ("cancelled", "Cancelled"),
            ("approved", "Approved"),
        ], default="draft", string="Status", track_visibility='onchange',
    )

    @api.multi
    def cancel(self):
        self.state = "cancelled"

    @api.multi
    def revert(self):
        print (5 * "\n")
        print (str(datetime.strptime(self.current_date, "%Y-%m-%d"))[:4])
        print (5 * "\n")
        self.state = "draft"

    @api.multi
    def calculate_increment(self):
        for record in self.employee_ids:
            wage = record.contract_reference.wage

            if self.use_x_percent_benefit:
                contract_date = datetime.strptime(record.contract_reference.date_start, "%Y-%m-%d")
                current_date = datetime.strptime(self.current_date, "%Y-%m-%d")

                delta = current_date - contract_date
                diff = float(delta.days) / 365.25

                if diff >= 5.00:
                    record.x_year_benefit = record.basic_wage * 0.02

            for config in self.increment_config.increment_config_line_ids:
                if config.starting_range <= wage < config.ending_range:
                    record.expected_salary_increment = ((wage * config.salary_increment) / 100) + config.offset
                if config.starting_range != 0 and config.ending_range == 0:
                    if wage >= config.starting_range:
                        record.expected_salary_increment = ((wage * config.salary_increment) / 100) + config.offset
                if config.ending_range != 0 and config.starting_range == 0:
                    if wage <= config.ending_range:
                        record.expected_salary_increment = ((wage * config.salary_increment) / 100) + config.offset

            if record.average_efficiency < 50:
                record.actual_salary_increment = record.expected_salary_increment * 0.6
                record.deduct = record.expected_salary_increment - record.actual_salary_increment
            elif 50 <= record.average_efficiency < 60:
                record.actual_salary_increment = record.expected_salary_increment * 0.7
                record.deduct = record.expected_salary_increment - record.actual_salary_increment
            elif 60 <= record.average_efficiency < 70:
                record.actual_salary_increment = record.expected_salary_increment * 0.8
                record.deduct = record.expected_salary_increment - record.actual_salary_increment
            elif 70 <= record.average_efficiency < 80:
                record.actual_salary_increment = record.expected_salary_increment * 0.95
                record.deduct = record.expected_salary_increment - record.actual_salary_increment
            elif 80 <= record.average_efficiency < 100:
                record.actual_salary_increment = record.expected_salary_increment * 1
                record.deduct = record.expected_salary_increment - record.actual_salary_increment

        self.state = "awaiting_approval"

    @api.multi
    def approve_increment(self):
        for record in self.employee_ids:
            total_increment = record.actual_salary_increment + record.punishment_return + record.x_year_benefit + record.award
            record.contract_reference.wage += total_increment

        self.state = "approved"

    @api.multi
    def populate_employees(self):
        # TODO unique constraint
        # self.increment_year = str(datetime.strptime(self.current_date, "%Y-%m-%d"))[:4]
        # for record in self:
        #     if record.department == self.department and record.increment_year == self.increment_year:
        #         raise Warning("This department has already been computed!\nPlease change the department")
        #     else:
        #         self.state = "input"

        if self.employee_ids:
            for record in self.employee_ids:
                record.unlink()
        emp = self.env['hr.employee'].search([])
        for record in emp:
            if not self.department.name:
                total_benefit = 0.00
                for rec in self.env['hr.contract'].browse(self._contract_find(record)):
                    for benefit in rec.benefit_line_ids:
                        total_benefit += benefit.employer_amount
                    basic_wage = rec.wage
                    gross_salary = total_benefit + rec.wage
                employee_data = {
                    "employee_name": record.id,
                    "contract_reference": self._contract_find(record),
                    "basic_wage": basic_wage,
                    "employee_benefit": total_benefit,
                    "gross_salary": gross_salary,
                    "efficiency_input_id": self.id,
                }
                employee_obj = self.env["employees.list"]
                employee_obj.create(employee_data)
            elif record.department_id.id == self.department.id:
                total_benefit = 0.00
                for rec in self.env['hr.contract'].browse(self._contract_find(record)):
                    for benefit in rec.benefit_line_ids:
                        total_benefit += benefit.employer_amount
                    basic_wage = rec.wage
                    gross_salary = total_benefit + rec.wage
                employee_data = {
                    "employee_name": record.id,
                    "contract_reference": self._contract_find(record),
                    "basic_wage": basic_wage,
                    "employee_benefit": total_benefit,
                    "gross_salary": gross_salary,
                    "efficiency_input_id": self.id,
                }
                employee_obj = self.env["employees.list"]
                employee_obj.create(employee_data)

    @api.multi
    def _contract_find(self, employee=None):
        """Finds the contract of the employee in question"""
        domain = [('employee_id', '=', employee.id)]

        contract_result = self.env['hr.contract'].search(domain, limit=1)

        contract_id = fields.Many2one('hr.contract')
        for record in contract_result:
            contract_id = record.id
        return contract_id

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code("salary_increment.record.seq")
        return super(EfficiencyInput, self).create(vals)

    @api.model
    def unlink(self):  # FIXME unlink issue
        for record in self:
            if record.state not in ("draft", "awaiting_approval"):
                raise Warning(_("You cannot delete a record that has been approved."))
        return super(EfficiencyInput, self).unlink()


class EmployeesList(models.Model):
    _name = 'employees.list'

    efficiency_input_id = fields.Many2one('efficiency.input')

    employee_name = fields.Many2one('hr.employee', sting='Employee Name', readonly=True)
    contract_reference = fields.Many2one('hr.contract', string='Contract Reference', readonly=True)
    basic_wage = fields.Float(string='Basic Salary', readonly=True)
    employee_benefit = fields.Float(string='Employee Benefit', readonly=True)
    gross_salary = fields.Float(string='Gross Salary', readonly=True)
    x_year_benefit = fields.Float(string='2% Benefit', readonly=True)
    efficiency_one = fields.Float(string='First assessment')
    efficiency_two = fields.Float(string='Second assessment')
    average_efficiency = fields.Float(string='Average Efficiency')
    expected_salary_increment = fields.Float(string='Expected Increment', readonly=True)
    actual_salary_increment = fields.Float(string='Actual Increment', readonly=True)
    deduct = fields.Float(string='Deduct', readonly=True)
    punishment_return = fields.Float(string='Punishment Return')
    award = fields.Float(string='Award')
    remark = fields.Text(string='Remark')

    @api.onchange('efficiency_one', 'efficiency_two')
    def _calculate_average_efficiency(self):
        if self.efficiency_one != 0.0:
            if self.efficiency_two != 0.0:
                self.average_efficiency = (self.efficiency_one + self.efficiency_two) / 2
            else:
                self.average_efficiency = self.efficiency_one
        else:
            if self.efficiency_two != 0.0:
                self.average_efficiency = self.efficiency_two
            else:
                self.average_efficiency = 0.0