
{
    'name': 'Access Restriction By IP',
    'summary': """User Can Access His Account Only From Specified IP Address""",
    'version': '15.0.1.0.0',
    'description': """User Can Access His Account Only From Specified IP Address""",
    'live_test_url': 'https://youtu.be/nn6dAL6eKPc',
    'author': 'ePillars',
    'company': 'ePillars Systems LLC',
    'website': 'https://www.epillars.com',
    'category': 'Tools',
    'depends': ['base', 'mail'],
    'license': 'AGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/allowed_ips_view.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
    'assets': {
        'web.assets_backend': [
            'access_restriction_by_ip/static/src/js/user_status.js',
        ],
    },
}

