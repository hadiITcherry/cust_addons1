# -*- coding: utf-8 -*-
{
    'name': "Realty Management",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com """,

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://portal.fake-agency.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','website'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'report/realty_property_report.xml',
        'views/views.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
