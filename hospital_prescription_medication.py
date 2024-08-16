from odoo import models, fields,api

class HospitalPrescriptionMedication(models.Model):
    _name = 'hospital.prescription.medication'
    _description = 'Prescription Medication'

    name = fields.Char(string='Medication', required=True)
    dosage = fields.Char(string='Dosage', required=True)
    instructions = fields.Char(string='Instructions')  # Not previously included, added for completeness
    prescription_id = fields.Many2one('hospital.prescription', string='Prescription',required=True)

