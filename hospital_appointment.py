import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import time, timedelta
from lxml import etree

_logger = logging.getLogger(__name__)


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'
    _rec_name = 'appointment_date'

    name = fields.Char(string='Appointment Reference', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    department_id = fields.Many2one('hospital.department', string='Department', required=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True,
                                domain="[('department_id', '=', department_id)]")
    appointment_date = fields.Datetime(string='Appointment Date', required=True)

    @api.onchange('department_id')
    def _onchange_department_id(self):
        self.doctor_id = False
        return {
            'domain': {'doctor_id': [('department_id', '=', self.department_id.id)]}
        }

    @api.constrains('appointment_date')
    def _check_appointment_date(self):
        for record in self:
            # Hafta sonu kontrolü
            if record.appointment_date.weekday() >= 5:  # 5 = Cumartesi, 6 = Pazar
                raise UserError("Randevu yalnızca hafta içi günlerde alınabilir.")

            # Saat kontrolü
            appointment_time = record.appointment_date.time()
            if not (
                    (time(6, 0) <= appointment_time < time(9, 30)) or
                    (time(10, 30) <= appointment_time < time(14, 0))
            ):
                raise UserError("Randevu saatleri hafta içi 09:00 - 12:30 ve 13:30 - 17:00 arasında olmalıdır.")

            # Çakışma kontrolü
            conflicting_appointments = self.search([
                ('id', '!=', record.id),
                ('department_id', '=', record.department_id.id),
                ('doctor_id', '=', record.doctor_id.id),
                ('appointment_date', '>=',
                 record.appointment_date.replace(second=0, microsecond=0) - timedelta(minutes=1)),  # Çakışma başlangıcı
                ('appointment_date', '<=',
                 record.appointment_date.replace(second=0, microsecond=0) + timedelta(minutes=1))  # Çakışma bitişi
            ])
            if conflicting_appointments:
                message = "Bu randevu saatine mevcut randevunuz bulunmaktadır."
                _logger.error(message)
                raise UserError(message)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        return super(HospitalAppointment, self).create(vals)


@api.model
def _get_appointment_domain(self):
    # Kayıt kuralı için alan belirleme
    if self.env.user.has_group('hospital_automation.group_hospital_doctor'):
        return [('doctor_id.user_id', '=', self.env.uid)]

    return []

 # doktorlar sadece kendi randevularını görsün.
@api.model
def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    res = super(HospitalAppointment, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                           submenu=submenu)

    user = self.env.user
    if user.has_group('hospital_automation.group_hospital_patient'):
        doc = etree.XML(res['arch'])
        for node in doc.xpath("//field[@name='patient_id']"):
            node.set('domain', "[('id', '=', %d)]" % user.id)
        res['arch'] = etree.tostring(doc, encoding='unicode')
    elif user.has_group('hospital_automation.group_hospital_doctor'):
        doc = etree.XML(res['arch'])
        for node in doc.xpath("//field[@name='doctor_id']"):
            node.set('domain', "[('id', '=', %d)]" % user.id)
        res['arch'] = etree.tostring(doc, encoding='unicode')
    return res

import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import time, timedelta
from lxml import etree

_logger = logging.getLogger(__name__)


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'
    _rec_name = 'appointment_date'

    name = fields.Char(string='Appointment Reference', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    department_id = fields.Many2one('hospital.department', string='Department', required=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True,
                                domain="[('department_id', '=', department_id)]")
    appointment_date = fields.Datetime(string='Appointment Date', required=True)

    @api.onchange('department_id')
    def _onchange_department_id(self):
        self.doctor_id = False
        return {
            'domain': {'doctor_id': [('department_id', '=', self.department_id.id)]}
        }

    @api.constrains('appointment_date')
    def _check_appointment_date(self):
        for record in self:
            # Hafta sonu kontrolü
            if record.appointment_date.weekday() >= 5:  # 5 = Cumartesi, 6 = Pazar
                raise UserError("Randevu yalnızca hafta içi günlerde alınabilir.")

            # Saat kontrolü
            appointment_time = record.appointment_date.time()
            if not (
                    (time(6, 0) <= appointment_time < time(9, 30)) or
                    (time(10, 30) <= appointment_time < time(14, 0))
            ):
                raise UserError("Randevu saatleri hafta içi 09:00 - 12:30 ve 13:30 - 17:00 arasında olmalıdır.")

            # Çakışma kontrolü
            conflicting_appointments = self.search([
                ('id', '!=', record.id),
                ('department_id', '=', record.department_id.id),
                ('doctor_id', '=', record.doctor_id.id),
                ('appointment_date', '>=',
                 record.appointment_date.replace(second=0, microsecond=0) - timedelta(minutes=1)),  # Çakışma başlangıcı
                ('appointment_date', '<=',
                 record.appointment_date.replace(second=0, microsecond=0) + timedelta(minutes=1))  # Çakışma bitişi
            ])
            if conflicting_appointments:
                message = "Bu randevu saatine mevcut randevunuz bulunmaktadır."
                _logger.error(message)
                raise UserError(message)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        return super(HospitalAppointment, self).create(vals)


@api.model
def _get_appointment_domain(self):
    # Kayıt kuralı için alan belirleme
    if self.env.user.has_group('hospital_automation.group_hospital_doctor'):
        return [('doctor_id.user_id', '=', self.env.uid)]

    return []

 # doktorlar sadece kendi randevularını görsün.
@api.model
def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    res = super(HospitalAppointment, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                           submenu=submenu)

    user = self.env.user
    if user.has_group('hospital_automation.group_hospital_patient'):
        doc = etree.XML(res['arch'])
        for node in doc.xpath("//field[@name='patient_id']"):
            node.set('domain', "[('id', '=', %d)]" % user.id)
        res['arch'] = etree.tostring(doc, encoding='unicode')
    elif user.has_group('hospital_automation.group_hospital_doctor'):
        doc = etree.XML(res['arch'])
        for node in doc.xpath("//field[@name='doctor_id']"):
            node.set('domain', "[('id', '=', %d)]" % user.id)
        res['arch'] = etree.tostring(doc, encoding='unicode')
    return res