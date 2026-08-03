"""Notifications Center API Router.

Exposes endpoints for user notifications, read receipts, and alert preferences.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/notifications", tags=["Notifications"])

# Endpoint placeholders (list_notifications, mark_as_read, update_preferences)
