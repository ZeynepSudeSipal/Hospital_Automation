from odoo import models, fields,api,_
from odoo.exceptions import UserError


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Hospital Doctor'

    name = fields.Char(string='Name', required=True)
    department_id = fields.Many2one('hospital.department', string='Department', required=True)
    phone = fields.Char(string='Phone')  # Telefon numarası için alan eklendi
    email = fields.Char(string='Email')  # E-posta için alan eklendi
    image = fields.Binary(string='Profile Image')  # Profil resmi için alan eklendi
    user_id = fields.Many2one('res.users', string='User', required=True, ondelete='cascade')

    def get_doctors(self):
        # Bu domain'i, tüm doktorları göstermek için değiştirdik
        domain = []
        return self.env['hospital.doctor'].search(domain)

    def _get_department_class(self):
        if self.department_id:
            return 'department-' + self.department_id.name.lower().replace(' ', '-')
        return''

    def _get_doctor_domain(self):
        if self.env.user.has_group('hospital_automation.group_hospital_doctor'):
            return [('user_id', '=', self.env.user.id)]

        return[]


