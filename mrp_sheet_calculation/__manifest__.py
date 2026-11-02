{
    'name': "MRP Sheet Calculation",
    'version': "0.1",

    'summary': "Extending the MRP workorder to automaltically calculate sheet required based on product configuration",

    'description': """
This customization extends the Manufacturing Order by automatically calculating sheet requirements based on product configuration (on the inventory tab).
The calculations are performed using the dimensions and productivity configured on the product    """,

    'author': "Odoo",
    'website': "https://www.Odoo.com",

    'category': 'Supply Chain/Manufacturing',

    'depends': ["base", "mrp", "hr"],
    'data': [
        'security/ir.access.csv',
        
        'views/mrp_production_views.xml',
        'views/mrp_workcenter_views.xml',
        'views/mrp_workorder_daily_production_views.xml',
        'views/mrp_workorder_views.xml',
        'views/product_template_views.xml'
    ],

}

