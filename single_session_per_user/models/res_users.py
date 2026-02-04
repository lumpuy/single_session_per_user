# -*- coding: utf-8 -*-
import logging
import os
import pickle
import json

from odoo import models
from odoo.http import root
from odoo.http import request

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = "res.users"

    @classmethod
    def _login(cls, db, credential, user_agent_env=None):
        """
        Override _login to force close all other sessions on new login.
        """
        # First do normal login
        auth_info = super()._login(db, credential, user_agent_env=user_agent_env)

        if auth_info and auth_info.get("uid"):
            try:
                uid = auth_info["uid"]
                _logger.info(f"User {uid} logged in - checking for other sessions")

                # Force close all other sessions for this user
                cls.force_close_all_user_sessions(uid)

            except Exception as e:
                _logger.error(f"Error in session cleanup: {e}")

        return auth_info

    @classmethod
    def force_close_all_user_sessions(cls, user_id):
        """
        Force close ALL sessions for a user except current one.
        Simple and effective approach.
        """
        try:
            session_store = root.session_store
            session_dir = getattr(session_store, "path", None)

            if not session_dir or not os.path.exists(session_dir):
                _logger.warning(f"Session directory not found: {session_dir}")
                return 0

            closed = 0
            user_str = str(user_id).encode()

            # Get current session ID if available
            current_sid = None
            if request and hasattr(request, "session"):
                current_sid = request.session.sid

            _logger.info(f"Searching sessions for user {user_id} in {session_dir}")

            for root_dir, dirs, files in os.walk(session_dir):
                for filename in files:
                    # Skip hidden/temp files
                    if filename.startswith(".") or filename.endswith("~"):
                        continue

                    file_path = os.path.join(root_dir, filename)

                    # Skip current session file
                    if current_sid and filename == current_sid:
                        _logger.debug(f"Skipping current session: {filename}")
                        continue

                    try:
                        # Read file and check if it belongs to our user
                        with open(file_path, "rb") as f:
                            content = f.read()

                        # Check if this session belongs to our user
                        if user_str in content:
                            # Additional check: try to parse session data
                            is_user_session = cls._is_user_session(content, user_id)

                            if is_user_session:
                                os.remove(file_path)
                                closed += 1
                                _logger.warning(f"✅ Closed session: {filename}")

                    except Exception as e:
                        _logger.debug(f"Could not process {filename}: {e}")

            if closed > 0:
                _logger.warning(
                    f"✅ Closed {closed} previous sessions for user {user_id}"
                )
            else:
                _logger.info(f"✅ No other sessions found for user {user_id}")

            return closed

        except Exception as e:
            _logger.error(f"Error closing sessions: {e}")
            return 0

    @classmethod
    def _is_user_session(cls, content, user_id):
        """
        Check if session content belongs to specific user.
        """
        try:
            # Try pickle format
            try:
                session_data = pickle.loads(content)
                if isinstance(session_data, dict):
                    session_uid = session_data.get("uid") or session_data.get("_uid")
                    if session_uid and int(session_uid) == user_id:
                        return True
            except:
                pass

            # Try JSON format
            try:
                decoded = content.decode("utf-8", errors="ignore")
                session_data = json.loads(decoded)
                if isinstance(session_data, dict):
                    session_uid = session_data.get("uid") or session_data.get("_uid")
                    if session_uid and int(session_uid) == user_id:
                        return True
            except:
                pass

            # Simple string check as fallback
            user_str = str(user_id)
            if f'"uid": {user_str}' in str(content) or f"'uid': {user_str}" in str(
                content
            ):
                return True

        except Exception as e:
            _logger.debug(f"Session validation error: {e}")

        return False
