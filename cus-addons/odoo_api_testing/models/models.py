
import calendar
import datetime
import json
from urllib.parse import urlencode
import urllib3
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

class OdooApiTesting(models.Model):
    _name = 'odoo.api.testing'
    _description = 'odoo_api_testing'
    _inherit="stock.picking"
    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()
    user_id = fields.Many2one('res.users', 'Current User', compute='_get_current_user')
    image = fields.Binary('odoo.api.testing')

    @api.model
    def _get_current_user(self):
      self.user_id = self.env.user.id

    def notify(self):
        check_state = self.env['stock.picking'].search([('partner_id','=',8)])
        states = []
        for state in check_state:
            states.append(state.state)
        if(check_state):
                raise ValidationError (states)
        else:
            pass

    
    def sendReq(self):
        check_state = self.env['stock.picking'].search([('origin','=',"S00007")])
        states = []
        for state in check_state:
            states = []
            states.append(state.state)
        if("done" in states):
                encoded_body = json.dumps({ "name": "done" })          
                http = urllib3.PoolManager()
                http.request("POST", "https://test-a5f09-default-rtdb.firebaseio.com/users.json", body=encoded_body, headers={"Content-Type":"application/json","auth":"ZA2AAsPGFTXUIG3IpYLRNXOkysISWMlTKJWQPH71"})
        if("assigned" in states):
                encoded_body = json.dumps({ "name": "assigned" })          
                http = urllib3.PoolManager()
                http.request("POST", "https://test-a5f09-default-rtdb.firebaseio.com/users.json", body=encoded_body, headers={"Content-Type":"application/json","auth":"ZA2AAsPGFTXUIG3IpYLRNXOkysISWMlTKJWQPH71"})
        if("waiting" in states):
                encoded_body = json.dumps({ "name": "done" })          
                http = urllib3.PoolManager()
                http.request("POST", "https://test-a5f09-default-rtdb.firebaseio.com/users.json", body=encoded_body, headers={"Content-Type":"application/json","auth":"ZA2AAsPGFTXUIG3IpYLRNXOkysISWMlTKJWQPH71"})
        else:
                pass

class ProductSpecification(models.Model):
        _name = "product.specification"
        product_id = fields.Many2one('product.template')

        size = fields.Selection([('64GB',"64GB"),('128GB',"128GB"),('256GB','256GB'),('512GB','512GB')],"Size",required=True)
        image = fields.Binary('product.specification')

class DeliveryModule(models.Model):
        _name="delivery.module"
        _inherit = "stock.picking"
        # name=fields.Char(computed="delivery_order")
        # partner_id=fields.Char(computed="customer")

        # def delivery_order(self):
        #         stock_pickin_id = self.env['stock.picking'].search([('user_id','=','2')])
        #         return stock_pickin_id.name
        
        # def customer(self):
        #         stock_pickin_id = self.env['stock.picking'].search([('user_id','=','2')])
        #         return stock_pickin_id.user_id.partner_id.name

class VipSubscribe(models.Model):
        _name="vip.subscribe"
        
        subscriber_id = fields.Many2one("res.partner","Subscriber")
        cost = fields.Float(string="Cost")
        start_date = fields.Date(string="Start Date")
        end_date = fields.Date(compute="calculate_end_date",string="End Date")

        def calculate_end_date(self):
                for s in self:
                        if s.start_date:
                           date_st = fields.Date.from_string(s.start_date)
                           dt = date_st + relativedelta(months=3) 
                           mounth = fields.Date.to_string(dt) 
                        s.update({'end_date': mounth})

class ProductTemplate(models.Model):
        _inherit = "product.template"

        vip = fields.Boolean(string="Is VIP")
        sale_price = fields.Float(string="Discount Price")
        vip_price = fields.Float(string="VIP price")

