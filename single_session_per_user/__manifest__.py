{
    'name': 'Single Session Per User - Force Logout Previous Sessions',
    'version': '18.0.1.0.1',
    'category': 'Tools/Security',
    'summary': 'Automatically close all previous sessions when user logs in from new device',
    'description': """
Single Session Per User
=======================
**Secure your Odoo instance by ensuring users have only one active session at a time**

Key Features:
-------------
✅ **Automatic Session Management**: When a user logs in from a new device, all previous sessions are immediately closed
✅ **Enhanced Security**: Prevent unauthorized access from multiple locations
✅ **Zero Configuration**: Works out of the box with Odoo's native session system
✅ **Odoo 18 Compatible**: Specifically designed for Odoo 18 Community Edition
✅ **Lightweight**: Minimal performance impact, no database changes required

How It Works:
-------------
1. User logs in from Chrome on office computer (Session A)
2. Same user logs in from Firefox at home (Session B)
3. **INSTANTLY**: Session A is automatically terminated
4. User can only maintain one active session at any time

Use Cases:
----------
- Companies requiring strict access control
- Preventing simultaneous logins from multiple locations
- Enhancing security for sensitive data
- Compliance with single-session policies

Technical Details:
------------------
- Uses Odoo's native session storage system
- Works at filesystem level for maximum reliability
- No external dependencies required
- Compatible with all Odoo 18 deployment methods

Note: This module is specifically designed for Odoo 18 Community Edition.
    """,
    'author': 'lumpuy@hotmail.com',
    'website': 'https://www.linkedin.com/in/luis-francisco-rojas-lumpuy-601b0413b/',
    'support': 'lumpuy@hotmail.com',
    'depends': ['base', 'web'],
    'data': [
        'security/ir_module_security.xml',
        'security/ir.model.access.csv',
    ],
    'images': [
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 10.00,
    'currency': 'USD',
    'license': 'OPL-1',
    'external_dependencies': {
        'python': [],
    },
    'pre_init_hook': None,
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': None,
}
