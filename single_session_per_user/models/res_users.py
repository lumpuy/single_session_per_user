# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.http import root, request
import os
import logging

_logger = logging.getLogger(__name__)


class UserSessionTracking(models.Model):
    _name = "res.users.session"
    _description = "User Session Tracking"

    user_id = fields.Many2one(
        "res.users", string="User", index=True, ondelete="cascade"
    )
    session_sid = fields.Char(string="Session ID", index=True)


class ResUsers(models.Model):
    _inherit = "res.users"

    @classmethod
    def _login(cls, db, credential, user_agent_env=None):
        auth_info = super()._login(db, credential, user_agent_env=user_agent_env)

        if auth_info and auth_info.get("uid"):
            uid = auth_info["uid"]
            if request and hasattr(request, "session"):
                current_sid = request.session.sid

                with cls.pool.cursor() as cr:
                    env = api.Environment(cr, uid, {})
                    Tracking = env["res.users.session"].sudo()

                    # 1. Get all session IDs to remove
                    old_sessions = Tracking.search(
                        [("user_id", "=", uid), ("session_sid", "!=", current_sid)]
                    )

                    if old_sessions:
                        session_store = root.session_store
                        # Get the physical path directly to bypass any Odoo cache
                        base_path = getattr(session_store, "path", None)

                        for s in old_sessions:
                            sid = s.session_sid
                            try:
                                # TRICK: Odoo 18 sometimes doesn't refresh session_store.delete()
                                # We force physical deletion from the filesystem
                                if base_path:
                                    # Odoo sessions are often nested: session_dir/s/e/session_id
                                    # session_store.get_session_filename handles the path nesting
                                    full_path = session_store.get_session_filename(sid)
                                    if os.path.exists(full_path):
                                        os.unlink(full_path)
                                        _logger.info(f"FORCED PHYSICAL DELETE: {sid}")

                                # Also tell Odoo's store to drop it from memory
                                session_store.delete(sid)
                            except Exception as e:
                                _logger.error(
                                    f"Failed to delete session file {sid}: {e}"
                                )

                        # 2. Delete from DB only after attempting disk deletion
                        old_sessions.unlink()

                    # 3. Register current session
                    Tracking.create({"user_id": uid, "session_sid": current_sid})
                    cr.commit()

        return auth_info
