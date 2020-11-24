# -*- coding: utf-8 -*-
from openerp import http

# class SalaryIncrement(http.Controller):
#     @http.route('/salary_increment/salary_increment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/salary_increment/salary_increment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('salary_increment.listing', {
#             'root': '/salary_increment/salary_increment',
#             'objects': http.request.env['salary_increment.salary_increment'].search([]),
#         })

#     @http.route('/salary_increment/salary_increment/objects/<model("salary_increment.salary_increment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('salary_increment.object', {
#             'object': obj
#         })