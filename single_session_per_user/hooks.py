# -*- coding: utf-8 -*-
import os
import pickle
import logging
import json
from odoo import api, tools

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    """
    Improved migration hook for Odoo 18.
    Handles both Pickle and JSON session formats.
    """
    from odoo.http import root
    from psycopg2.extras import execute_values

    cr = env.cr
    session_store = root.session_store

    # Strategy 1: Get path from session_store
    session_dir = getattr(session_store, "path", None)

    # Strategy 2: Fallback to Odoo standard data dir if Strategy 1 fails
    if not session_dir or not os.path.exists(session_dir):
        session_dir = os.path.join(tools.config["data_dir"], "sessions")

    _logger.info("Checking session directory: %s", session_dir)

    if not session_dir or not os.path.exists(session_dir):
        _logger.error("CRITICAL: Session directory NOT FOUND at %s", session_dir)
        return

    session_data_list = []
    processed = 0
    errors = 0

    _logger.info("Starting disk scan...")

    for root_dir, dirs, files in os.walk(session_dir):
        for filename in files:
            # Basic Odoo session file validation
            if filename.startswith(".") or len(filename) < 10:
                continue

            file_path = os.path.join(root_dir, filename)
            uid = None

            try:
                with open(file_path, "rb") as f:
                    content = f.read()
                    if not content:
                        continue

                    # Try Pickle (Traditional Odoo)
                    try:
                        data = pickle.loads(content)
                        uid = data.get("uid")
                    except:
                        # Try JSON (Modern/Modified Odoo)
                        try:
                            data = json.loads(content.decode("utf-8"))
                            uid = data.get("uid")
                        except:
                            pass

                if uid:
                    session_data_list.append((int(uid), filename))
                    processed += 1

                # Batch insert to DB
                if len(session_data_list) >= 1000:
                    execute_values(
                        cr,
                        "INSERT INTO res_users_session (user_id, session_sid) VALUES %s",
                        session_data_list,
                    )
                    session_data_list = []
                    _logger.info("Migrated %s sessions...", processed)

            except Exception as e:
                errors += 1
                continue

    # Final batch
    if session_data_list:
        execute_values(
            cr,
            "INSERT INTO res_users_session (user_id, session_sid) VALUES %s",
            session_data_list,
        )

    cr.commit()  # Force commit for the hook
    _logger.info(
        "MIGRATION FINISHED: %s sessions indexed, %s errors.", processed, errors
    )
