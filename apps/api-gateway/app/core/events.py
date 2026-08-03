"""Application Lifetime Event Listeners and Callbacks.

Provides explicit event hook placeholders for application lifecycle management.
"""

import logging

logger = logging.getLogger("talentai.events")


async def on_startup() -> None:
    """Execute startup lifecycle actions."""
    logger.info("Executing custom startup event listeners...")


async def on_shutdown() -> None:
    """Execute shutdown cleanup actions."""
    logger.info("Executing custom shutdown event listeners...")
