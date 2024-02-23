from datetime import date, datetime
from hashlib import md5
import json
from odoo import http

class OdooApiTesting(http.Controller):        
    ### Get User Info
    @http.route('/api/getUser', auth='user',type='http',csrf=False,website=False,methods=['GET'])
    def get_user_info(self):
        users = http.request.env['res.users'].sudo().search([('id','=',http.request.env.user.id)])
        user_list = []
        headers = {'Content-Type': 'application/json'}
        for user in users:
            user_dat = http.request.env['res.partner'].sudo().search([('id','=',user.partner_id.id)])
            user_list.append({
                'id':user.partner_id.id,
                'name':str(list(map(lambda u:u.name, user_dat))[0]),
                'email':str(list(map(lambda u:u.email, user_dat))[0]),
                'mobile':str(list(map(lambda u:u.mobile, user_dat))[0]),
                'street':str(list(map(lambda u:u.street, user_dat))[0]),
                'street2':str(list(map(lambda u:u.street2, user_dat))[0]),
                'zip':str(list(map(lambda u:u.zip, user_dat))[0]),
                'city':str(list(map(lambda u:u.city, user_dat))[0]),
            })
        return  http.Response(json.dumps({"success":True,"code":200,"data":user_list}), headers=headers)

    ### Update user info 
    @http.route('/api/updateUserInfo',auth="user" , type='json',csrf=False,methods=['PUT'])
    def update_user(self,**kw):
        user = http.request.env['res.users'].sudo().search([('id',"=",http.request.env.user.id)])
        if (user):
            for record in user:
                user_data = http.request.env['res.partner'].sudo().search([('id','=',record.partner_id.id)])
                record.write({
                        "name":kw['name'],
                        "login":kw['login']
                        })
                for rec in user_data:
                    rec.write({
                        "mobile":kw['mobile'],
                        "dob":kw['dob']
                    })
            return {
                "status":"Success"
            }
        return {
            "status":"Failed"
        }

    #### Register User
    @http.route('/api/register', auth='public',type='json',csrf=False,methods=['POST'])
    def register(self,**kw):
        user_password = kw['password']
        email = kw['login']
        if http.request.env["res.users"].sudo().search([("login", "=", email)]):
            return {"status":"Failed, user already exist!"}
        http.request.env['res.users'].sudo().create({
                'name':kw['name'],
                'password':user_password,
                'login':email,
            })
        return {
            "status":"Succesfully Registered"
        }

    ### login user
    @http.route('/api/login', type='json', auth="none",csrf=False,methods=["POST"])
    def authenticate(self,**kw):
        email = kw['login'],
        password = kw['password']
        http.request.session.authenticate("odoo", email, password)
        return {
        "status":"Successfully Logged in"
        }
        
    ### Logout
    @http.route('/api/logout', type='http', auth="user",csrf=False)
    def destroy(self):
        http.request.session.logout()

    ### Product
    @http.route('/api/getProducts', auth='none',type='http',csrf=False,methods=['GET'])
    def get_products(self):
        products = http.request.env['product.template'].sudo().search([])
        product_details = []
        headers = {'Content-Type': 'application/json'}
        for product in products:
            attributes = http.request.env['product.template.attribute.value'].sudo().search([('product_tmpl_id.id','=',product.id)])
            images = http.request.env['product.image'].sudo().search([('product_tmpl_id.id','=',product.id)])
            product_details.append({
                'id':product.id,
                'name':product.name,
                'product_qty':product.qty_available,
                'images':list(map(lambda img:(img.image_1920).decode('utf-8'), images)),
                'price':product.list_price,
                'type':product.detailed_type,
                'policy':product.invoice_policy,
                'category':product.categ_id.name,
                'description':product.description_sale,
                "specifications":dict(map(lambda attr:(attr.attribute_id.name,attr.product_attribute_value_id.name), attributes))
            })
        return http.Response(json.dumps({"success":True,"code":200,"data":product_details}), headers=headers)
        
    @http.route('/api/getProductsf', auth='none',type='json',csrf=False,methods=['POST'])
    def get_products_filtered(self,**kw):
        page_number = int(kw['page'])
        per_page = 3
        offset = 0 if page_number <= 1 else (page_number - 1) * per_page
        products = http.request.env['product.template'].sudo().search([],offset=offset,limit=per_page)
        product_details = []
        for product in products:
            attributes = http.request.env['product.template.attribute.value'].sudo().search([('product_tmpl_id.id','=',product.id)])
            images = http.request.env['product.image'].sudo().search([('product_tmpl_id.id','=',product.id)])
            product_details.append({
                'name':product.name,
                'product_qty':product.qty_available,
                'images':list(map(lambda img:(img.image_1920).decode('utf-8'), images)),
                'price':product.list_price,
                'type':product.detailed_type,
                'policy':product.invoice_policy,
                'category':product.categ_id.name,
                'description':product.description_sale,
                "specifications":dict(map(lambda attr:(attr.attribute_id.name,attr.product_attribute_value_id.name), attributes))
            })
            pagination = {
                "page":page_number if page_number > 0 else 1,
                "size":per_page
            }
        return {"success":True,"code":200,"data":product_details,"pagination":pagination}
        
    ### Get Product By id (single page)
    @http.route('/api/getProducts/<id>', auth='none',type='http',csrf=False,methods=['GET'])
    def get_products_by_id(self,id):
        products = http.request.env['product.template'].sudo().search([("id",'=',id)])
        product_details = []
        headers = {'Content-Type': 'application/json'}
        for product in products:
            attributes = http.request.env['product.template.attribute.value'].sudo().search([('product_tmpl_id.id','=',product.id)])
            images = http.request.env['product.image'].sudo().search([('product_tmpl_id.id','=',product.id)])
            product_details.append({
                'id':product.id,
                'name':product.name,
                'product_qty':product.qty_available,
                'images':list(map(lambda img:(img.image_1920).decode('utf-8'), images)),
                'price':product.list_price,
                'type':product.detailed_type,
                'policy':product.invoice_policy,
                'category':product.categ_id.name,
                'description':product.description_sale,
                "specifications":dict(map(lambda attr:(attr.attribute_id.name,attr.product_attribute_value_id.name), attributes))
            })
        return http.Response(json.dumps({"success":True,"code":200,"data":product_details}), headers=headers)
    
    ### Get all categories
    @http.route('/api/getCategories',auth='none',type='http',csrf=False,methods=['GET'])
    def get_Categories(self):
        category = http.request.env['product.category'].sudo().search([])
        categories = []
        headers = {'Content-Type':"application/json"}
        for categ in category:
            sub_category = http.request.env['product.category'].sudo().search([("id",'=',categ.parent_id.id)])
            categories.append({
                "id":categ.id,
                "category":categ.name,
                "parent":''.join([str(c.name) for c in sub_category])
            })
        return http.Response(json.dumps({"success":True,"code":200,"data":categories}), headers=headers)

    ### Get category by id
    @http.route('/api/getCategories/<id>',auth='none',type='http',csrf=False,methods=['GET'])
    def get_Categories_by_id(self,id):
        category = http.request.env['product.category'].sudo().search([('id','=',id)])
        categories = []
        headers = {'Content-Type':"application/json"}
        for categ in category:
            sub_category = http.request.env['product.category'].sudo().search([("id",'=',categ.parent_id.id)])
            categories.append({
                "id":categ.id,
                "category":categ.name,
                "parent":''.join([str(c.name) for c in sub_category])
            })
        return http.Response(json.dumps({"success":True,"code":200,"data":categories}), headers=headers)
    
    ### Get all brands 
    @http.route('/api/getBrands',auth='none',type='http',csrf=False,methods=['GET'])
    def get_brands(self):
        brand = http.request.env['product.attribute'].sudo().search([('name','=',"Brand")])
        brands = []
        headers = {'Content-Type':"application/json"}
        for brand in brand:
            brand_values = http.request.env['product.attribute.value'].sudo().search([('attribute_id.id','=',brand.id)])
            for b in brand_values:
                brands.append({
                    "id":b.id,
                    "brand":b.name
                })
        return http.Response(json.dumps({"success":True,"code":200,"data":brands}), headers=headers)
   
   ### Get brands by id
    @http.route('/api/getBrands/<id>',auth='none',type='http',csrf=False,methods=['GET'])
    def get_brands_by_id(self,id):
        brand_values = http.request.env['product.attribute.value'].sudo().search([('id','=',id)])
        brands = []
        headers = {'Content-Type':"application/json"}
        for brand in brand_values:
            brands.append({
                "id":brand.id,
                "brand":brand.name
            })
        return http.Response(json.dumps({"success":True,"code":200,"data":brands}), headers=headers)
   
    ### Order Details
    @http.route('/api/getOrders',auth='user',type='http',csrf=False,methods=['GET'],)
    def get_order_details(self):
        orders = http.request.env['sale.order'].sudo().search([('user_id.id','=',http.request.env.user.id)]) 
        order_list = []
        headers = {'Content-Type': 'application/json'}
        for order in orders:
            order_lines = http.request.env['sale.order.line'].sudo().search([('order_id.id','=',order.id)]) 
            order_list.append({
                        'id':order.id,
                        'order':order.name,
                        'username':order.partner_id.name,
                        'email':order.partner_id.email,
                        'street':order.partner_id.street,
                        'street2':order.partner_id.street2,
                        'zip':order.partner_id.zip,
                        'city':order.partner_id.city,
                        'mobile':order.partner_id.mobile,
                        'invoice_status':order.invoice_status,
                        'product':''.join(list(map(lambda ol:ol.name, order_lines))),
                        'price_total':float((''.join([str(ol.price_total) for ol in order_lines])).strip() or 0),
                        'quantity':float((''.join([str(ol.product_uom_qty) for ol in order_lines])).strip() or 0)
                    })        
        return http.Response(json.dumps({"success":True,"code":200,"data":order_list}), headers=headers)

    ### Order Details by Id
    @http.route('/api/getOrders/<id>',auth='user',type='http',csrf=False,methods=['GET'],)
    def get_order_details(self,id):
        orders = http.request.env['sale.order'].sudo().search([('id','=',id)]) 
        order_list = []
        headers = {'Content-Type': 'application/json'}
        for order in orders:
            order_lines = http.request.env['sale.order.line'].sudo().search([('order_id.id','=',order.id)]) 
            order_list.append({
                        'id':order.id,
                        'order':order.name,
                        'username':order.partner_id.name,
                        'email':order.partner_id.email,
                        'street':order.partner_id.street,
                        'street2':order.partner_id.street2,
                        'zip':order.partner_id.zip,
                        'city':order.partner_id.city,
                        'mobile':order.partner_id.mobile,
                        'invoice_status':order.invoice_status,
                        'product':''.join(list(map(lambda ol:ol.name, order_lines))),
                        'price_total':float((''.join([str(ol.price_total) for ol in order_lines])).strip() or 0),
                        'quantity':float((''.join([str(ol.product_uom_qty) for ol in order_lines])).strip() or 0)
                    })        
        return http.Response(json.dumps({"success":True,"code":200,"data":order_list}), headers=headers)

    ### Create Delivery Order
    @http.route('/api/deliveryOrder/<id>',auth="user",type="json",csrf=False,methods=["POST"])
    def create_delivery_order(self,id,**kw):
        user = http.request.env['res.users'].sudo().search([('id',"=",http.request.env.user.id)])
        order = http.request.env['sale.order'].sudo().create({
            'partner_id': int(''.join([str(pi.partner_id.id) for pi in user])),
            'user_id': int(''.join([str(pi.id) for pi in user])),
            'partner_invoice_id':int(''.join([str(pi.partner_id.id) for pi in user])),
            'partner_shipping_id':int(''.join([str(pi.partner_id.id) for pi in user])),
            'date_order':datetime.now(),
            'invoice_status':"to invoice",
            'state':"sale",
            "website_id":1
        })
        order_id = order
        product_id = int(id)
        product = http.request.env['product.template'].sudo().search([('id','=',product_id)])
        order_line = http.request.env['sale.order.line'].sudo().create({
            'order_id':order_id.id,
            'product_id': product_id,
            'name':''.join([str(name.name) for name in product]),
            'product_uom_qty':kw['product_uom_qty'],
            'price_unit': float((''.join([str(pu.list_price) for pu in product])).strip() or 0),
            'invoice_status':'to invoice'
        })
        return {
            'status':'success'
        }

   ### Create Online Payment Order
    @http.route('/api/opOrder/<id>',auth="user",type="json",csrf=False,methods=["POST"])
    def create_online_payment_order(self,id,**kw):
        user = http.request.env['res.users'].sudo().search([('id',"=",http.request.env.user.id)])
        order = http.request.env['sale.order'].sudo().create({
            'partner_id': int(''.join([str(pi.partner_id.id) for pi in user])),
            'user_id': int(''.join([str(pi.id) for pi in user])),
            'partner_invoice_id':int(''.join([str(pi.partner_id.id) for pi in user])),
            'partner_shipping_id':int(''.join([str(pi.partner_id.id) for pi in user])),
            'date_order':datetime.now(),
            "website_id":1,
            "state":"sale"
        })
        order_id = order
        product_id = int(id)
        product = http.request.env['product.template'].sudo().search([('id','=',product_id)])
        order_line = http.request.env['sale.order.line'].sudo().create({
            'order_id':order_id.id,
            'product_id': product_id,
            'name':''.join([str(name.name) for name in product]),
            'product_uom_qty':kw['product_uom_qty'],
            'price_unit': float((''.join([str(pu.list_price) for pu in product])).strip() or 0),
        })
        return {
            'status':'success'
        }
    
    ### Get Delivery Addresses
    @http.route('/api/getDeliveryAddresses',auth="user" , type='http',csrf=False,methods=['GET'])
    def get_addresses(self):
        address = http.request.env['res.partner'].sudo().search([('id','=',http.request.env.user.partner_id.id)])
        main={}
        other = []
        headers = {'Content-Type': 'application/json'}
        for add in address:
            main = {
                    "id":add.id,
                    "name":add.name,
                    "street":add.street,
                    "street2":add.street2,
                    "country":add.country_id.name,
                    "city":add.city,
                    "zip":add.zip,
                    "mobile":add.mobile
            }
            child_address = http.request.env['res.partner'].sudo().search([('parent_id.id',"=",add.id)])
            for child in child_address:
                other.append({
                    "id":child.id,
                    "name":child.name,
                    "street":child.street,
                    "street2":child.street2,
                    "country":child.country_id.name,
                    "city":child.city,
                    "zip":child.zip,
                    "mobile":child.mobile
                })
        return http.Response(json.dumps({"success":True,"code":200,"data":{"default":main,"other":other}}), headers=headers)
    
    ### Get Delivery Addresses By Id
    @http.route('/api/getDeliveryAddresses/<id>',auth="user" , type='http',csrf=False,methods=['GET'])
    def get_addresses_by_id(self,id):
        address = http.request.env['res.partner'].sudo().search([('id','=',id)])
        main={}
        headers = {'Content-Type': 'application/json'}
        for add in address:
            main = {
                    "id":add.id,
                    "name":add.name,
                    "street":add.street,
                    "street2":add.street2,
                    "country":add.country_id.name,
                    "city":add.city,
                    "zip":add.zip,
                    "mobile":add.mobile
            }
        return http.Response(json.dumps({"success":True,"code":200,"data":main}), headers=headers)
    
    ### Update Delivery Address
    @http.route('/api/updateDeliveryAddress/<id>',auth="user" , type='json',csrf=False,methods=['PUT'])
    def update_address(self,id,**kw):
        user = http.request.env['res.partner'].sudo().search([('id',"=",id)])
        if (user):
            for record in user:
                record.write({
                    "name":kw['name'],
                    "street":kw['street'],
                    "street2":kw['street2'],
                    "city":kw['city'],
                    "zip":kw['zip'],
                    "mobile":kw['mobile']
                    })
                return {
                        "status":"Success"
                    }
        return {
            "status":"Failed"
        }
    ### Create Delivery Address
    @http.route('/api/createDeliveryAddress', auth='user',type='json',csrf=False,website=False,methods=['POST'])
    def create_delivery_address(self,**kw):
        user = http.request.env['res.partner'].sudo().search([('id',"=",http.request.env.user.partner_id.id)])
        http.request.env['res.partner'].sudo().create({
            'parent_id': user.id,
            'type': "delivery",
            "name":kw['name'],
            "street":kw['street'],
            "street2":kw['street2'],
            "country_id":126,
            "city":kw['city'],
            "zip":kw['zip'],
            "mobile":kw['mobile']
            })
        return {
            "status":"success"
        }

    ### Get service types
    @http.route('/api/getServiceTypes',auth="none" , type='http',csrf=False,methods=['GET'])
    def get_service_types(self):
        service = http.request.env['fsm.order.type'].sudo().search([])
        services = []
        headers = {'Content-Type': 'application/json'}
        for serv in service:
            services.append({
                "id":serv.id,
                "type":serv.name
            })
        return http.Response(json.dumps({"success":True,"code":200,"data":services}), headers=headers)
    
    ### Get service types
    @http.route('/api/getServiceTypes/<id>',auth="none" , type='http',csrf=False,methods=['GET'])
    def get_service_types_by_id(self,id):
        service = http.request.env['fsm.order.type'].sudo().search([("id","=",id)])
        services = []
        headers = {'Content-Type': 'application/json'}
        for serv in service:
            services.append({
                "id":serv.id,
                "type":serv.name
            })
        return http.Response(json.dumps({"success":True,"code":200,"data":services}), headers=headers)
    
    ### get services 
    @http.route('/api/getServices',auth="none" , type='http',csrf=False,methods=['GET'])
    def get_service(self):
        service = http.request.env['fsm.tag'].sudo().search([])
        services = []
        headers = {'Content-Type': 'application/json'}
        for serv in service:
            services.append({
                "id":serv.id,
                "service":serv.name
            })
        return http.Response(json.dumps({"success":True,"code":200,"data":services}), headers=headers)

    ### get services 
    @http.route('/api/getServices/<id>',auth="none" , type='http',csrf=False,methods=['GET'])
    def get_service_by_id(self,id):
        service = http.request.env['fsm.tag'].sudo().search([("id","=",id)])
        services = []
        headers = {'Content-Type': 'application/json'}
        for serv in service:
            services.append({
                "id":serv.id,
                "service":serv.name
            })
        return http.Response(json.dumps({"success":True,"code":200,"data":services}), headers=headers)
    
    ### Get Delivery state
    @http.route('/api/getState',auth="user" , type='http',csrf=False,methods=['GET'])
    def get_state_by_id(self):
        states = http.request.env['stock.picking'].sudo().search([('partner_id.id','=',http.request.env.user.partner_id.id)])
        states_list = []
        headers = {'Content-Type':"application/json"}
        for state in states:
            states_list = []
            states_list.append({
                "partner_id":state.partner_id.id,
                "state":state.state
            })
        return http.Response(json.dumps({"success":True,"code":200,"data":states_list}), headers=headers)
    
    ### Accept Request
    @http.route('/api/accpetRequest', auth='public',type='json',csrf=False,website=False,methods=['POST'])
    def test_get_delivery_states(self):
        http.request.env['fsm.order'].sudo().write({
                'stage_id':4
        }) 
        
    ### Reject Request
    @http.route('/api/rejectRequest', auth='public',type='json',csrf=False,website=False,methods=['POST'])
    def test_get_delivery_states(self):
        http.request.env['fsm.order'].sudo().write({
                'stage_id':3
        })    
    
    ### Repair Form
    @http.route('/api/repairService', auth='user',type='json',csrf=False,website=False,methods=['POST'])
    def repair_form(self,**kw):
        user = http.request.env['res.users'].sudo().search([('id',"=",http.request.env.user.id)])
        http.request.env['fsm.order'].sudo().create({
            'partner_id': int(''.join([str(pi.partner_id.id) for pi in user])),
            'type': kw['type'],
            'tag_ids':[(4,kw['tag_ids'])],
            'delivery_type':kw['delivery_type'],
            'description':kw['description'],
        })
        return {
            "status":"success"
        }
    
    ### Data Recover Form
    @http.route('/api/dataRecoverService', auth='public',type='json',csrf=False,website=False,methods=['POST'])
    def data_recovery_form(self,**kw):
        user = http.request.env['res.users'].sudo().search([('id',"=",http.request.env.user.id)])
        http.request.env['fsm.order'].sudo().create({
            'partner_id': int(''.join([str(pi.partner_id.id) for pi in user])),
            'type': kw['type'],
            'tag_ids':[(4,kw['tag_ids'])],
            'delivery_type':kw['delivery_type'],
            'description':kw['description'],
        })
        return {
            "status":"success"
        }
    
    ### Maintenance Form
    @http.route('/api/maintenance', auth='public',type='json',csrf=False,website=False,methods=['POST'])
    def maintenance(self,**kw):
        user = http.request.env['res.users'].sudo().search([('id',"=",http.request.env.user.id)])
        http.request.env['fsm.order'].sudo().create({
            'partner_id': int(''.join([str(pi.partner_id.id) for pi in user])),
            'type': kw['type'],
            'tag_ids':[(4,kw['tag_ids'])],
            'delivery_type':kw['delivery_type'],
            'description':kw['description'],
        })
        return {
            "status":"success"
        }
    
    ### IT Services Form
    @http.route('/api/ITServices', auth='public',type='json',csrf=False,website=False,methods=['POST'])
    def it_services(self,**kw):
        user = http.request.env['res.users'].sudo().search([('id',"=",http.request.env.user.id)])
        http.request.env['fsm.order'].sudo().create({
            'partner_id': int(''.join([str(pi.partner_id.id) for pi in user])),
            'type': kw['type'],
            'tag_ids':[(4,kw['tag_ids'])],
            'delivery_type':kw['delivery_type'],
            'description':kw['description'],
        })
        return {
            "status":"success"
        }

    
   