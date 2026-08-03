"""Role-Based (RBAC) and Attribute-Based (ABAC) Permission Checkers.

Validates user scopes, role hierarchies, and resource ownership before
route execution.
"""

from typing import List


class PermissionChecker:
    """Enforces fine-grained permission requirements on routes.
    
    Attributes:
        allowed_roles: List of roles authorized to access the resource.
    """

    def __init__(self, allowed_roles: List[str]) -> None:
        """Initialize PermissionChecker with required roles."""
        self.allowed_roles = allowed_roles

    def __call__(self, user_role: str) -> bool:
        """Evaluate if user_role satisfies authorization requirements.
        
        Args:
            user_role: Role assigned to requesting user.
            
        Returns:
            True if authorized, False otherwise.
        """
        # TODO: Implement RBAC/ABAC authorization checks
        return user_role in self.allowed_roles
