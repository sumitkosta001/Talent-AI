"""Company Directory API Router.

Exposes endpoints for company exploration, company profile details, reviews, and tech stacks.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/companies", tags=["Companies"])

# Endpoint placeholders (list_companies, get_company_by_id, update_company_profile)
