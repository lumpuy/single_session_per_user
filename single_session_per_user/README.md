# Single Session Per User for Odoo 18

## Overview
This module ensures that each user can only have one active session at a time. When a user logs in from a new device or browser, all previous sessions are automatically terminated.

## Features
- 🔒 **Automatic session termination** on new login
- 🛡️ **Enhanced security** for your Odoo instance
- ⚡ **Instant operation** - no delays
- 🎯 **Odoo 18 Community Edition** compatibility
- 🏗️ **No database changes** required

## Installation
1. Download the module
2. Extract to your Odoo addons directory
3. Update module list in Odoo
4. Install "Single Session Per User"

## Configuration
No configuration needed! The module works out of the box.

## How It Works
The module hooks into Odoo's authentication system and monitors session files. When a user authenticates, it checks for existing sessions and removes them.

## Support
For support, contact: lumpuy@hotmail.com

## License
Odoo Proprietary License v1.0 (OPL-1)