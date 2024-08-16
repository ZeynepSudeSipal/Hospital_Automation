from odoo import models, fields, api, _


class HospitalPrescription(models.Model):
    _name = 'hospital.prescription'
    _description = 'Hospital Prescription'
    _rec_name = 'name'

    name = fields.Char(string='Prescription Reference', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    doctor_department_id = fields.Many2one(related='doctor_id.department_id', string='Doctor Department', store=True,
                                           readonly=True)
    date = fields.Datetime(string='Date', default=fields.Datetime.now, required=True)
    medication_ids = fields.One2many('hospital.prescription.medication', 'prescription_id', string='Medications')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.prescription') or _('New')
        return super(HospitalPrescription, self).create(vals)

    def action_print_prescription(self):
        return self.env.ref('hospital_automation.action_report_prescription').report_action(self)

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        user = self.env.user
        if user.has_group('hospital_automation.group_hospital_patient'):
            patient = self.env['hospital.patient'].search([('user_id', '=', user.id)], limit=1)
            if patient:
                args += [('patient_id', '=', patient.id)]
            else:
                args += [('patient_id', '=', False)]
        return super(HospitalPrescription, self)._search(args, offset, limit, order, count)


    @api.onchange('doctor_id')
    def _onchange_doctor(self):
        if self.env.user.has_group('hospital_automation.group_hospital_doctor'):
            return {
                'domain': {'doctor_id': [('user_id', '=', self.env.uid)]}
            }

    @api.model
    def default_get(self, fields_list):
        res = super(HospitalPrescription, self).default_get(fields_list)
        if self.env.user.has_group('hospital_automation.group_hospital_doctor'):
            doctor = self.env['hospital.doctor'].search([('user_id', '=', self.env.user.id)], limit=1)
            if doctor:
                res['doctor_id'] = doctor.id

        return res