from odoo import models, fields, api, _
from odoo.exceptions import UserError


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'
    _rec_name = 'display_name'

    name = fields.Char(string='Name', required=True)
    surname = fields.Char(string='Surname', required=True)
    tc = fields.Char(string='TC', required=True)
    phone = fields.Char(string='Phone', required=True)
    email = fields.Char(string='Email', required=True)
    password = fields.Char(string='Password', required=True)
    user_id = fields.Many2one('res.users', string='User', required=True, ondelete='cascade')
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', ondelete='set null',
                                help='Doctor assigned to the patient')


    display_name = fields.Char(string='Display Name', compute='_compute_display_name')

    @api.depends('name', 'surname')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.name} {record.surname}"



