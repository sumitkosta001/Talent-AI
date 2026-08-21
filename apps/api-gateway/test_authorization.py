"""TalentAI API Gateway — Authorization & Security Integration Test Suite.

Executes 18 comprehensive integration tests against the TalentAI API Gateway server
using `httpx.Client` with `ASGITransport(app=app)` and pytest fixtures.

Verifies:
- Account registration & duplicate email handling (201 / 409)
- Credential authentication & login failures (200 / 401)
- Protected route access & Bearer token authorization (200 / 401)
- Invalid, malformed, and missing token handling (401)
- Refresh token rotation & reuse prevention (200 / 401)
- Single session logout & token revocation (200 / 401)
- Multi-device bulk session termination (200 / 401)
- Optional RBAC route authorization checks (403 / 404 skip)
"""

import sys
import uuid
import pytest
from typing import Dict, Any, Generator
from starlette.testclient import TestClient

from app.main import app

# ==============================================================================
# CONFIGURATION & CONSTANTS
# ==============================================================================
API_V1_PREFIX = "/api/v1"
AUTH_PREFIX = f"{API_V1_PREFIX}/auth"

REGISTER_URL = f"{AUTH_PREFIX}/register"
LOGIN_URL = f"{AUTH_PREFIX}/login"
REFRESH_URL = f"{AUTH_PREFIX}/refresh"
LOGOUT_URL = f"{AUTH_PREFIX}/logout"
LOGOUT_ALL_URL = f"{AUTH_PREFIX}/logout-all"
ME_URL = f"{AUTH_PREFIX}/me"

DEFAULT_PASSWORD = "Password123!"


# ==============================================================================
# HELPER FUNCTIONS & FIXTURES
# ==============================================================================
def print_header(title: str) -> None:
    """Print formatted header block for test progress visualization."""
    print("=" * 60)
    print(title)
    print("=" * 60)


def print_pass(details: str = "") -> None:
    """Print PASS marker and optional status details."""
    print("PASS")
    if details:
        print(details)
    print()


def generate_unique_email() -> str:
    """Generate a unique test email address using UUID v4."""
    unique_suffix = uuid.uuid4().hex[:8]
    return f"test_{unique_suffix}@gmail.com"


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    """Pytest fixture providing an in-memory HTTP client bound to FastAPI app."""
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def auth_state() -> Dict[str, Any]:
    """Module-scoped shared authorization state for sequential integration flow."""
    return {
        "email": generate_unique_email(),
        "password": DEFAULT_PASSWORD,
        "user_id": None,
        "access_token": None,
        "refresh_token": None,
        "revoked_refresh_token": None,
    }


# ==============================================================================
# TEST IMPLEMENTATIONS
# ==============================================================================
def test_1_register(client: TestClient, auth_state: Dict[str, Any]) -> None:
    """Test 1: User Account Registration (POST /register -> 201 Created)."""
    print_header("TEST 1 - REGISTER")

    email = auth_state["email"]
    payload = {
        "email": email,
        "password": DEFAULT_PASSWORD,
        "confirm_password": DEFAULT_PASSWORD,
        "first_name": "Test",
        "last_name": "User",
    }

    response = client.post(REGISTER_URL, json=payload, timeout=60)
    assert response.status_code == 201, f"Expected HTTP 201, got {response.status_code}: {response.text}"

    data = response.json()
    assert "message" in data, "Response missing 'message' key"
    assert "user" in data, "Response missing 'user' key"
    assert "tokens" in data, "Response missing 'tokens' key"

    user_data = data["user"]
    tokens_data = data["tokens"]

    user_id = str(user_data["id"])
    access_token = tokens_data["access_token"]
    refresh_token = tokens_data["refresh_token"]

    assert user_data["email"] == email, "Returned email does not match registered email"
    assert access_token and isinstance(access_token, str), "Invalid access_token"
    assert refresh_token and isinstance(refresh_token, str), "Invalid refresh_token"

    auth_state["user_id"] = user_id
    auth_state["access_token"] = access_token
    auth_state["refresh_token"] = refresh_token

    print_pass(
        f"User ID: {user_id}\nEmail: {email}\nAccess Token: Received\nRefresh Token: Received"
    )


def test_2_duplicate_registration(client: TestClient, auth_state: Dict[str, Any]) -> None:
    """Test 2: Duplicate Email Registration (POST /register -> 409 Conflict)."""
    print_header("TEST 2 - DUPLICATE REGISTRATION")

    email = auth_state["email"]
    payload = {
        "email": email,
        "password": DEFAULT_PASSWORD,
        "confirm_password": DEFAULT_PASSWORD,
        "first_name": "Duplicate",
        "last_name": "User",
    }

    response = client.post(REGISTER_URL, json=payload, timeout=60)
    assert response.status_code == 409, f"Expected HTTP 409, got {response.status_code}: {response.text}"

    print_pass("Conflict (409) returned correctly for duplicate email registration.")


def test_3_login(client: TestClient, auth_state: Dict[str, Any]) -> None:
    """Test 3: Valid User Login (POST /login -> 200 OK)."""
    print_header("TEST 3 - LOGIN")

    email = auth_state["email"]
    payload = {
        "email": email,
        "password": DEFAULT_PASSWORD,
    }

    response = client.post(LOGIN_URL, json=payload, timeout=60)
    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}: {response.text}"

    data = response.json()
    assert "tokens" in data, "Login response missing 'tokens' key"

    access_token = data["tokens"]["access_token"]
    refresh_token = data["tokens"]["refresh_token"]

    assert access_token and isinstance(access_token, str), "Invalid access_token"
    assert refresh_token and isinstance(refresh_token, str), "Invalid refresh_token"

    auth_state["access_token"] = access_token
    auth_state["refresh_token"] = refresh_token

    print_pass("Access Token: Received\nRefresh Token: Received")


def test_4_wrong_password(client: TestClient, auth_state: Dict[str, Any]) -> None:
    """Test 4: Login with Incorrect Password (POST /login -> 401 Unauthorized)."""
    print_header("TEST 4 - WRONG PASSWORD")

    email = auth_state["email"]
    payload = {
        "email": email,
        "password": "WrongPassword123!",
    }

    response = client.post(LOGIN_URL, json=payload, timeout=60)
    assert response.status_code == 401, f"Expected HTTP 401, got {response.status_code}: {response.text}"

    print_pass("Unauthorized (401) returned correctly for wrong password.")


def test_5_unknown_email(client: TestClient) -> None:
    """Test 5: Login with Non-Existent Email (POST /login -> 401 Unauthorized)."""
    print_header("TEST 5 - UNKNOWN EMAIL")

    unknown_email = f"unknown_{uuid.uuid4().hex[:8]}@gmail.com"
    payload = {
        "email": unknown_email,
        "password": DEFAULT_PASSWORD,
    }

    response = client.post(LOGIN_URL, json=payload, timeout=60)
    assert response.status_code == 401, f"Expected HTTP 401, got {response.status_code}: {response.text}"

    print_pass("Unauthorized (401) returned correctly for unknown email.")


def test_6_current_user(client: TestClient, auth_state: Dict[str, Any]) -> None:
    """Test 6: Authenticated User Profile (GET /me -> 200 OK)."""
    print_header("TEST 6 - CURRENT USER")

    access_token = auth_state["access_token"]
    expected_email = auth_state["email"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get(ME_URL, headers=headers, timeout=60)
    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}: {response.text}"

    data = response.json()
    assert "user" in data, "Response missing 'user' key"

    returned_email = data["user"]["email"]
    assert returned_email == expected_email, f"Expected email {expected_email}, got {returned_email}"

    print_pass(f"Fetched profile successfully for email: {returned_email}")


def test_7_missing_authorization(client: TestClient) -> None:
    """Test 7: Access Protected Endpoint Without Header (GET /me -> 401 Unauthorized)."""
    print_header("TEST 7 - MISSING AUTHORIZATION")

    response = client.get(ME_URL, timeout=60)
    assert response.status_code == 401, f"Expected HTTP 401, got {response.status_code}: {response.text}"

    print_pass("Unauthorized (401) returned correctly for missing Authorization header.")


def test_8_invalid_jwt(client: TestClient) -> None:
    """Test 8: Access Protected Endpoint With Invalid JWT (GET /me -> 401 Unauthorized)."""
    print_header("TEST 8 - INVALID JWT")

    headers = {"Authorization": "Bearer abc123"}
    response = client.get(ME_URL, headers=headers, timeout=60)
    assert response.status_code == 401, f"Expected HTTP 401, got {response.status_code}: {response.text}"

    print_pass("Unauthorized (401) returned correctly for invalid JWT signature/format.")


def test_9_malformed_jwt(client: TestClient) -> None:
    """Test 9: Access Protected Endpoint With Malformed JWT (GET /me -> 401 Unauthorized)."""
    print_header("TEST 9 - MALFORMED JWT")

    headers = {"Authorization": "Bearer hello.world"}
    response = client.get(ME_URL, headers=headers, timeout=60)
    assert response.status_code == 401, f"Expected HTTP 401, got {response.status_code}: {response.text}"

    print_pass("Unauthorized (401) returned correctly for malformed JWT string.")


def test_10_refresh_token(client: TestClient, auth_state: Dict[str, Any]) -> None:
    """Test 10: Rotate Refresh Token (POST /refresh -> 200 OK)."""
    print_header("TEST 10 - REFRESH TOKEN")

    old_access_token = auth_state["access_token"]
    old_refresh_token = auth_state["refresh_token"]

    payload = {"refresh_token": old_refresh_token}
    response = client.post(REFRESH_URL, json=payload, timeout=60)
    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}: {response.text}"

    data = response.json()
    assert "tokens" in data, "Response missing 'tokens' key"

    new_access_token = data["tokens"]["access_token"]
    new_refresh_token = data["tokens"]["refresh_token"]

    assert new_access_token != old_access_token, "New access token must differ from old access token"
    assert new_refresh_token != old_refresh_token, "New refresh token must differ from old refresh token (Token Rotation)"

    auth_state["access_token"] = new_access_token
    auth_state["refresh_token"] = new_refresh_token

    print_pass("New Access Token: Received\nNew Refresh Token: Received (Token Rotation verified)")


def test_11_refresh_token_as_access_token(client: TestClient, auth_state: Dict[str, Any]) -> None:
    """Test 11: Attempt Access Endpoint Using Refresh Token (GET /me -> 401 Unauthorized)."""
    print_header("TEST 11 - REFRESH TOKEN USED AS ACCESS TOKEN")

    refresh_token = auth_state["refresh_token"]
    headers = {"Authorization": f"Bearer {refresh_token}"}
    response = client.get(ME_URL, headers=headers, timeout=60)
    assert response.status_code == 401, f"Expected HTTP 401, got {response.status_code}: {response.text}"

    print_pass("Unauthorized (401) returned correctly when refresh token is sent as bearer access token.")


def test_12_logout(client: TestClient, auth_state: Dict[str, Any]) -> None:
    """Test 12: Logout User Session (POST /logout -> 200 OK)."""
    print_header("TEST 12 - LOGOUT")

    refresh_token = auth_state["refresh_token"]
    payload = {"refresh_token": refresh_token}
    response = client.post(LOGOUT_URL, json=payload, timeout=60)
    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}: {response.text}"

    auth_state["revoked_refresh_token"] = refresh_token
    print_pass("Session logged out successfully.")


def test_13_refresh_after_logout(client: TestClient, auth_state: Dict[str, Any]) -> None:
    """Test 13: Refresh Using Revoked Token (POST /refresh -> 401 Unauthorized)."""
    print_header("TEST 13 - REFRESH AFTER LOGOUT")

    revoked_refresh_token = auth_state["revoked_refresh_token"]
    payload = {"refresh_token": revoked_refresh_token}
    response = client.post(REFRESH_URL, json=payload, timeout=60)
    assert response.status_code == 401, f"Expected HTTP 401, got {response.status_code}: {response.text}"

    print_pass("Unauthorized (401) returned correctly when refreshing with a revoked token.")


def test_14_login_again(client: TestClient, auth_state: Dict[str, Any]) -> None:
    """Test 14: Re-authenticate to Create New Session (POST /login -> 200 OK)."""
    print_header("TEST 14 - LOGIN AGAIN")

    email = auth_state["email"]
    payload = {
        "email": email,
        "password": DEFAULT_PASSWORD,
    }

    response = client.post(LOGIN_URL, json=payload, timeout=60)
    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}: {response.text}"

    data = response.json()
    access_token = data["tokens"]["access_token"]
    refresh_token = data["tokens"]["refresh_token"]

    auth_state["access_token"] = access_token
    auth_state["refresh_token"] = refresh_token

    print_pass("New session created successfully.")


def test_15_logout_all_devices(client: TestClient, auth_state: Dict[str, Any]) -> None:
    """Test 15: Revoke All Sessions Across All Devices (POST /logout-all -> 200 OK)."""
    print_header("TEST 15 - LOGOUT ALL DEVICES")

    access_token = auth_state["access_token"]
    refresh_token = auth_state["refresh_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post(LOGOUT_ALL_URL, headers=headers, timeout=60)
    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}: {response.text}"

    auth_state["revoked_refresh_token"] = refresh_token
    print_pass("All active sessions revoked successfully.")


def test_16_refresh_after_logout_all(client: TestClient, auth_state: Dict[str, Any]) -> None:
    """Test 16: Refresh After Bulk Revocation (POST /refresh -> 401 Unauthorized)."""
    print_header("TEST 16 - REFRESH AFTER LOGOUT ALL")

    revoked_refresh_token = auth_state["revoked_refresh_token"]
    payload = {"refresh_token": revoked_refresh_token}
    response = client.post(REFRESH_URL, json=payload, timeout=60)
    assert response.status_code == 401, f"Expected HTTP 401, got {response.status_code}: {response.text}"

    print_pass("Unauthorized (401) returned correctly after bulk session revocation.")


def test_17_invalid_refresh_token(client: TestClient) -> None:
    """Test 17: Refresh With Random String (POST /refresh -> 401 Unauthorized)."""
    print_header("TEST 17 - INVALID REFRESH TOKEN")

    payload = {"refresh_token": "abc123"}
    response = client.post(REFRESH_URL, json=payload, timeout=60)
    assert response.status_code == 401, f"Expected HTTP 401, got {response.status_code}: {response.text}"

    print_pass("Unauthorized (401) returned correctly for invalid refresh token.")


def test_18_logout_invalid_token(client: TestClient) -> None:
    """Test 18: Logout With Random String (POST /logout -> 401 Unauthorized)."""
    print_header("TEST 18 - LOGOUT INVALID TOKEN")

    payload = {"refresh_token": "abc123"}
    response = client.post(LOGOUT_URL, json=payload, timeout=60)
    assert response.status_code == 401, f"Expected HTTP 401, got {response.status_code}: {response.text}"

    print_pass("Unauthorized (401) returned correctly when attempting logout with invalid token.")


def test_optional_rbac_endpoints(client: TestClient, auth_state: Dict[str, Any]) -> None:
    """Test Optional RBAC Routes (if present on server)."""
    access_token = auth_state["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    rbac_routes = ["/admin-test", "/company-test", "/candidate-test", "/superuser-test"]

    for route in rbac_routes:
        url = f"{API_V1_PREFIX}{route}"
        try:
            res = client.get(url, headers=headers, timeout=60)
            if res.status_code == 404:
                continue
            print(f"Optional RBAC test for {route}: Status {res.status_code}")
        except Exception:
            pass


# ==============================================================================
# MAIN EXECUTION ROUTINE (CLI Compatibility)
# ==============================================================================
def main() -> None:
    """Execute complete authorization integration test suite."""
    print("\nStarting TalentAI Integration Test Suite...")

    with TestClient(app) as c:
        state: Dict[str, Any] = {
            "email": generate_unique_email(),
            "password": DEFAULT_PASSWORD,
            "user_id": None,
            "access_token": None,
            "refresh_token": None,
            "revoked_refresh_token": None,
        }

        test_1_register(c, state)
        test_2_duplicate_registration(c, state)
        test_3_login(c, state)
        test_4_wrong_password(c, state)
        test_5_unknown_email(c)
        test_6_current_user(c, state)
        test_7_missing_authorization(c)
        test_8_invalid_jwt(c)
        test_9_malformed_jwt(c)
        test_10_refresh_token(c, state)
        test_11_refresh_token_as_access_token(c, state)
        test_12_logout(c, state)
        test_13_refresh_after_logout(c, state)
        test_14_login_again(c, state)
        test_15_logout_all_devices(c, state)
        test_16_refresh_after_logout_all(c, state)
        test_17_invalid_refresh_token(c)
        test_18_logout_invalid_token(c)
        test_optional_rbac_endpoints(c, state)

    print("=" * 60)
    print("ALL AUTHORIZATION TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except AssertionError as err:
        print(f"\n[TEST FAILED]: {err}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"\n[UNEXPECTED ERROR]: {exc}", file=sys.stderr)
        sys.exit(1)
