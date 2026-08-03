"""OAuth2 Social Authentication Integration Handlers.

Manages authorization code flows for external OAuth identity providers
(Google Workspace, GitHub, LinkedIn).
"""

from typing import Any, Dict


class OAuth2Provider:
    """Base interface for OAuth2 identity providers."""

    def get_authorization_url(self, state: str) -> str:
        """Construct external OAuth authorization redirect URL.
        
        Args:
            state: Anti-CSRF verification state token.
            
        Returns:
            Fully qualified authorization redirect URL.
        """
        # TODO: Implement OAuth provider redirect URL generator
        return "https://accounts.google.com/o/oauth2/v2/auth?client_id=PLACEHOLDER"

    async def fetch_user_profile(self, code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token and fetch user info.
        
        Args:
            code: Authorization code returned from OAuth callback.
            
        Returns:
            Normalized user profile dictionary (email, name, avatar).
        """
        # TODO: Implement token exchange via httpx async client
        return {"email": "user@example.com", "name": "Alex Johnson", "provider": "google"}
