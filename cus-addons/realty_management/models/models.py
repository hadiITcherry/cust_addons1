from odoo import models, fields, api , Command
from datetime import date,datetime
from ....exceptions import ValidationError 

class RealtyProperty(models.Model):
    _name = 'realty.property'
    _description = 'realty.property'

    name = fields.Char(required=True)
    consturction_date = fields.Date(required=True)
    rent = fields.Float(required=True)
    rooms = fields.Integer(required=True)
    parking_slots = fields.Integer(required=True)
    surface = fields.Float(required=True)
    furnishing = fields.Boolean(required=True)
    address = fields.Char(required=True)
    available = fields.Boolean(required=True)
    is_rented = fields.Boolean(compute="_check_time_frame",required=True,default=False)

    def _check_time_frame(self):
       check_date = self.env['realty.tenancy'].search([('start_date','<=',fields.Date.today())])
       if(self.available):
            if (check_date):
                    self.is_rented = True
            else:
                    self.is_rented = False  
       else:
            self.is_rented = False  

    def action_custom_url_property(self):
         return {
            'type': 'ir.actions.act_url',
            'name': 'Redirect to Website',
            'url': 'https://portal.fake-agency.com/properties/'+str(self.id),
            'target': 'new'
        }  

class RealtyTenant(models.Model):
    _name = 'realty.tenant'
    _description = "realty.tenant"
    
    partner_id = fields.Many2one('res.partner')
    
    name = fields.Char(related="partner_id.name")
    phone = fields.Char(related="partner_id.phone")
    email = fields.Char(related="partner_id.email")


class RealtyTenancy(models.Model):
    _name = "realty.tenancy"
    _description = "realty.tenancy"

    property_id = fields.Many2one('realty.property', 'Property')
    tenant_id = fields.Many2one('realty.tenant', 'Tenant')

    property_ids = fields.Many2many("realty.property","property_tenancy","property_id",limit=1)
    tenant_ids = fields.Many2many("realty.tenant","property_tenant","tenant_id",limit=1)

    contract_name = fields.Char(compute="_get_contract_name")
    start_date = fields.Date(required=True)
    end_date = fields.Date()
    state = fields.Selection([('draft', 'Draft'),('active', 'Active'),('terminated', 'Terminated'),('cancelled','Cancelled')],'State',default="draft",required=True)
    
    @api.depends('tenant_ids','property_ids')
    def _get_contract_name(self):
            for rec in self:
                if ((rec.property_ids != "") & (rec.tenant_ids != "")):
                    self.contract_name =  str(rec.property_ids.name or '') + ' ' +str(rec.tenant_ids.name or '')
                elif ((rec.property_ids != "") & (rec.tenant_ids == "")):
                    self.contract_name =  str(rec.property_ids.name)
                else:
                    self.computed_char_field = ''
    
    def change_state(self):
        if (self.end_date != ""):
            if (self.end_date > self.start_date):
                self.write({
                    'state': 'active'
                })
            else:
                raise ValidationError("Check Date !")
        else:
            raise ValidationError("No End Date !")

    def terminate_state(self):
        if(self.state != "terminated"):
            self.write({
                'state':'terminated'
            })
        else:
            pass

    @api.model
    def update_tenancy_state(self):
      check_date = self.env['realty.tenancy'].search([('end_date','=',fields.Date.today())])
      check_date.write({
                'state':'terminated'
            })
    
    def action_custom_url_tenancy(self):
        return {
            'type': 'ir.actions.act_url',
            'name': 'Redirect to Website',
            'url': 'https://portal.fake-agency.com/tenancies/'+str(self.id),
            'target': 'new'
        }
    
    
    def action_cancel_tenancy(self):
        if(self.state != 'terminated'):
            self.write({
                'state': 'cancelled',
                'tenant_ids':[
                        Command.clear()
                    ]
            })
        else:
            pass

    @api.model
    def create(self, vals):
        self._assign_default_tenant(vals)
        return super(RealtyTenancy,self).create(vals)

    def _assign_default_tenant(self, vals):
        tenant_vals = {"name":"Default User","email":"user@agency.test"}
        vals.update({
            'tenant_ids':[
                (5,0,0),
                (0,0,tenant_vals)
            ]
        })



class RealtyTenancyLines (models.AbstractModel):
    _inherit="realty.tenancy"

    product = fields.Selection([('rent',"Rent"),('bills',"Bills")],"Product",required=True)
    quantity = fields.Integer(required=True)
    price = fields.Float(required=True)
    total_amount = fields.Float(compute="_calculate_total_amount",readonly=True)

    @api.depends('quantity','price')
    def _calculate_total_amount(self):
        if ( (self.quantity != "") & (self.price != "")):
            self.total_amount = self.quantity * self.price
        else:
            raise ValidationError ("Quantity and Price cat be empty!")


class ResPartner (models.Model):
    _inherit = "res.partner"

    dob = fields.Date()
    pob = fields.Char()
    nationality = fields.Char()