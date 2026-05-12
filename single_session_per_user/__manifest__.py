{
    'name': 'Single Session Per User - Force Logout Previous Sessions',
    'version': '18.0.1.0.2',
    'category': 'Tools/Security',
    'summary': 'Automatically close all previous sessions when user logs in from new device',
    'description': """
Single Session Per User
=======================
**Secure your Odoo instance by ensuring users have only one active session at a time**

Key Features:
-------------
✅ **Automatic Session Management**: When a user logs in from a new device, all previous sessions are immediately closed
✅ **Group-Based Exclusions (New)**: Define specific groups (e.g., Administrators) that are exempt from the single-session rule.
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
5. **Excluded User**: If a user belongs to a group with the "Exclude Single Session" flag, they can maintain multiple active sessions.
6. **Instant Transition**: If you remove a user from an excluded group, the single-session restriction applies to them on their next activity.

Use Cases:
----------
- Companies requiring strict access control for general staff.
- Allowing IT Administrators or Power Users to work from multiple devices simultaneously.
- Preventing simultaneous logins from shared accounts.
- Enhancing security for sensitive data while maintaining flexibility for key roles.

Technical Details:
------------------
- Uses Odoo's native session storage system
- Works at filesystem level for maximum reliability
- No external dependencies required
- Compatible with all Odoo 18 deployment methods
- Adds `exclude_single_session` to `res.groups`.

Note: This module is specifically designed for Odoo 18 Community Edition.
    """,
    'author': 'lumpuy@hotmail.com',
    'website': 'https://www.linkedin.com/in/luis-francisco-rojas-lumpuy-601b0413b/',
    'support': 'lumpuy@hotmail.com',
    'depends': ['base', 'web'],
    'data': [
        'security/ir_module_security.xml',
        'security/ir.model.access.csv',
        'views/res_groups_views.xml',
    ],
    "images": ["static/description/background.png", ],
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
