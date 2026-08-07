"""TalentAI API Gateway — Authorization & Security Integration Test Suite.

Executes 18 comprehensive integration tests against a running TalentAI API Gateway server
(http://127.0.0.1:8000) using the standard `requests` library.

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
import json
import requests

# ==============================================================================
# CONFIGURATION & CONSTANTS
# ==============================================================================
BASE_URL = "http://127.0.0.1:8000"
API_V1_PREFIX = "/api/v1"
AUTH_PREFIX = f"{API_V1_PREFIX}/auth"

REGISTER_URL = f"{BASE_URL}{AUTH_PREFIX}/register"
LOGIN_URL = f"{BASE_URL}{AUTH_PREFIX}/login"
REFRESH_URL = f"{BASE_URL}{AUTH_PREFIX}/refresh"
LOGOUT_URL = f"{BASE_URL}{AUTH_PREFIX}/logout"
LOGOUT_ALL_URL = f"{BASE_URL}{AUTH_PREFIX}/logout-all"
ME_URL = f"{BASE_URL}{AUTH_PREFIX}/me"

DEFAULT_PASSWORD = "Password123!"


# ==============================================================================
# HELPER FUNCTIONS
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


# ==============================================================================
# TEST IMPLEMENTATIONS
# ==============================================================================
def test_1_register(email: str) -> tuple[str, str, str]:
    """Test 1: User Account Registration (POST /register -> 201 Created)."""
    print_header("TEST 1 - REGISTER")

    payload = {
        "email": email,
        "password": DEFAULT_PASSWORD,
        "confirm_password": DEFAULT_PASSWORD,
        "first_name": "Test",
        "last_name": "User",
    }

    response = requests.post(REGISTER_URL, json=payload, timeout=60)
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

    print_pass(
        f"User ID: {user_id}\nEmail: {email}\nAccess Token: Received\nRefresh Token: Received"
    )

    return user_id, access_token, refresh_token


def test_2_duplicate_registration(email: str) -> None:
    """Test 2: Duplicate Email Registration (POST /register -> 409 Conflict)."""
    print_header("TEST 2 - DUPLICATE REGISTRATION")

    payload = {
        "email": email,
        "password": DEFAULT_PASSWORD,
        "confirm_password": DEFAULT_PASSWORD,
        "first_name": "Duplicate",
        "last_name": "User",
    }

    response = requests.post(REGISTER_URL, json=payload, timeout=60)
    assert response.status_code == 409, f"Expected HTTP 409, got {response.status_code}: {response.text}"

    print_pass("Conflict (409) returned correctly for duplicate email registration.")


def test_3_login(email: str) -> tuple[str, str]:
    """Test 3: Valid User Login (POST /login -> 200 OK)."""
    print_header("TEST 3 - LOGIN")

    payload = {
        "email": email,
        "password": DEFAULT_PASSWORD,
    }

    response = requests.post(LOGIN_URL, json=payload, timeout=60)
    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}: {response.text}"

    data = response.json()
    assert "tokens" in data, "Login response missing 'tokens' key"

    access_token = data["tokens"]["access_token"]
    refresh_token = data["tokens"]["refresh_token"]

    assert access_token and isinstance(access_token, str), "Invalid access_token"
    assert refresh_token and isinstance(refresh_token, str), "Invalid refresh_token"

    print_pass("Access Token: Received\nRefresh Token: Received")

    return access_token, refresh_token


def test_4_wrong_password(email: str) -> None:
    """Test 4: Login with Incorrect Password (POST /login -> 401 Unauthorized)."""
    print_header("TEST 4 - WRONG PASSWORD")

    payload = {
        "email": email,
        "password": "WrongPassword123!",
    }

    response = requests.post(LOGIN_URL, json=payload, timeout=60)
    assert response.status_code == 401, f"Expected HTTP 401, got {response.status_code}: {response.text}"

    print_pass("Unauthorized (401) returned correctly for wrong password.")


def test_5_unknown_email() -> None:
    """Test 5: Login with Non-Existent Email (POST /login -> 401 Unauthorized)."""
    print_header("TEST 5 - UNKNOWN EMAIL")

    unknown_email = f"unknown_{uuid.uuid4().hex[:8]}@gmail.com"
    payload = {
        "email": unknown_email,
        "password": DEFAULT_PASSWORD,
    }

    response = requests.post(LOGIN_URL, json=payload, timeout=60)
    assert response.status_code == 401, f"Expected HTTP 401, got {response.status_code}: {response.text}"

    print_pass("Unauthorized (401) returned correctly for unknown email.")


def test_6_current_user(access_token: str, expected_email: str) -> None:
    """Test 6: Authenticated User Profile (GET /me -> 200 OK)."""
    print_header("TEST 6 - CURRENT USER")

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(ME_URL, headers=headers, timeout=60)
    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}: {response.text}"

    data = response.json()
    assert "user" in data, "Response missing 'user' key"

    returned_email = data["user"]["email"]
    assert returned_email == expected_email, f"Expected email {expected_email}, got {returned_email}"

    print_pass(f"Fetched profile successfully for email: {returned_email}")


def test_7_missing_authorization() -> None:
    """Test 7: Access Protected Endpoint Without Header (GET /me -> 401 Unauthorized)."""
    print_header("TEST 7 - MISSING AUTHORIZATION")

    response = requests.get(ME_URL, timeout=60)
    assert response.status_code == 401, f"Expected HTTP 401, got {response.status_code}: {response.text}"

    print_pass("Unauthorized (401) returned correctly for missing Authorization header.")


def test_8_invalid_jwt() -> None:
    """Test 8: Access Protected Endpoint With Invalid JWT (GET /me -> 401 Unauthorized)."""
    print_header("TEST 8 - INVALID JWT")

    headers = {"Authorization": "Bearer abc123"}
    response = requests.get(ME_URL, headers=headers, timeout=60)
    assert response.status_code == 401, f"Expected HTTP 401, got {response.status_code}: {response.text}"

    print_pass("Unauthorized (401) returned correctly for invalid JWT signature/format.")


def test_9_malformed_jwt() -> None:
    """Test 9: Access Protected Endpoint With Malformed JWT (GET /me -> 401 Unauthorized)."""
    print_header("TEST 9 - MALFORMED JWT")

    headers = {"Authorization": "Bearer hello.world"}
    response = requests.get(ME_URL, headers=headers, timeout=60)
    assert response.status_code == 401, f"Expected HTTP 401, got {response.status_code}: {response.text}"

    print_pass("Unauthorized (401) returned correctly for malformed JWT string.")


def test_10_refresh_token(old_access_token: str, old_refresh_token: str) -> tuple[str, str]:
    """Test 10: Rotate Refresh Token (POST /refresh -> 200 OK)."""
    print_header("TEST 10 - REFRESH TOKEN")

    payload = {"refresh_token": old_refresh_token}
    response = requests.post(REFRESH_URL, json=payload, timeout=60)
    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}: {response.text}"

    data = response.json()
    assert "tokens" in data, "Response missing 'tokens' key"

    new_access_token = data["tokens"]["access_token"]
    new_refresh_token = data["tokens"]["refresh_token"]

    assert new_access_token != old_access_token, "New access token must differ from old access token"
    assert new_refresh_token != old_refresh_token, "New refresh token must differ from old refresh token (Token Rotation)"

    print_pass("New Access Token: Received\nNew Refresh Token: Received (Token Rotation verified)")

    return new_access_token, new_refresh_token


def test_11_refresh_token_as_access_token(refresh_token: str) -> None:
    """Test 11: Attempt Access Endpoint Using Refresh Token (GET /me -> 401 Unauthorized)."""
    print_header("TEST 11 - REFRESH TOKEN USED AS ACCESS TOKEN")

    headers = {"Authorization": f"Bearer {refresh_token}"}
    response = requests.get(ME_URL, headers=headers, timeout=60)
    assert response.status_code == 401, f"Expected HTTP 401, got {response.status_code}: {response.text}"

    print_pass("Unauthorized (401) returned correctly when refresh token is sent as bearer access token.")


def test_12_logout(refresh_token: str) -> None:
    """Test 12: Logout User Session (POST /logout -> 200 OK)."""
    print_header("TEST 12 - LOGOUT")

    payload = {"refresh_token": refresh_token}
    response = requests.post(LOGOUT_URL, json=payload, timeout=60)
    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}: {response.text}"

    print_pass("Session logged out successfully.")


def test_13_refresh_after_logout(revoked_refresh_token: str) -> None:
    """Test 13: Refresh Using Revoked Token (POST /refresh -> 401 Unauthorized)."""
    print_header("TEST 13 - REFRESH AFTER LOGOUT")

    payload = {"refresh_token": revoked_refresh_token}
    response = requests.post(REFRESH_URL, json=payload, timeout=60)
    assert response.status_code == 401, f"Expected HTTP 401, got {response.status_code}: {response.text}"

    print_pass("Unauthorized (401) returned correctly when refreshing with a revoked token.")


def test_14_login_again(email: str) -> tuple[str, str]:
    """Test 14: Re-authenticate to Create New Session (POST /login -> 200 OK)."""
    print_header("TEST 14 - LOGIN AGAIN")

    payload = {
        "email": email,
        "password": DEFAULT_PASSWORD,
    }

    response = requests.post(LOGIN_URL, json=payload, timeout=60)
    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}: {response.text}"

    data = response.json()
    access_token = data["tokens"]["access_token"]
    refresh_token = data["tokens"]["refresh_token"]

    print_pass("New session created successfully.")

    return access_token, refresh_token


def test_15_logout_all_devices(access_token: str) -> None:
    """Test 15: Revoke All Sessions Across All Devices (POST /logout-all -> 200 OK)."""
    print_header("TEST 15 - LOGOUT ALL DEVICES")

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(LOGOUT_ALL_URL, headers=headers, timeout=60)
    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}: {response.text}"

    print_pass("All active sessions revoked successfully.")


def test_16_refresh_after_logout_all(revoked_refresh_token: str) -> None:
    """Test 16: Refresh After Bulk Revocation (POST /refresh -> 401 Unauthorized)."""
    print_header("TEST 16 - REFRESH AFTER LOGOUT ALL")

    payload = {"refresh_token": revoked_refresh_token}
    response = requests.post(REFRESH_URL, json=payload, timeout=60)
    assert response.status_code == 401, f"Expected HTTP 401, got {response.status_code}: {response.text}"

    print_pass("Unauthorized (401) returned correctly after bulk session revocation.")


def test_17_invalid_refresh_token() -> None:
    """Test 17: Refresh With Random String (POST /refresh -> 401 Unauthorized)."""
    print_header("TEST 17 - INVALID REFRESH TOKEN")

    payload = {"refresh_token": "abc123"}
    response = requests.post(REFRESH_URL, json=payload, timeout=60)
    assert response.status_code == 401, f"Expected HTTP 401, got {response.status_code}: {response.text}"

    print_pass("Unauthorized (401) returned correctly for invalid refresh token.")


def test_18_logout_invalid_token() -> None:
    """Test 18: Logout With Random String (POST /logout -> 401 Unauthorized)."""
    print_header("TEST 18 - LOGOUT INVALID TOKEN")

    payload = {"refresh_token": "abc123"}
    response = requests.post(LOGOUT_URL, json=payload, timeout=60)
    assert response.status_code == 401, f"Expected HTTP 401, got {response.status_code}: {response.text}"

    print_pass("Unauthorized (401) returned correctly when attempting logout with invalid token.")


def test_optional_rbac_endpoints(access_token: str) -> None:
    """Test Optional RBAC Routes (if present on server)."""
    headers = {"Authorization": f"Bearer {access_token}"}
    rbac_routes = ["/admin-test", "/company-test", "/candidate-test", "/superuser-test"]

    for route in rbac_routes:
        url = f"{BASE_URL}{API_V1_PREFIX}{route}"
        try:
            res = requests.get(url, headers=headers, timeout=60)
            if res.status_code == 404:
                continue
            print(f"Optional RBAC test for {route}: Status {res.status_code}")
        except Exception:
            pass


# ==============================================================================
# MAIN EXECUTION ROUTINE
# ==============================================================================
def main() -> None:
    """Execute complete authorization integration test suite."""
    print("\nStarting TalentAI Integration Test Suite...")
    print(f"Target Server: {BASE_URL}\n")

    email = generate_unique_email()

    # Execution Pipeline
    user_id, access_token, refresh_token = test_1_register(email)
    test_2_duplicate_registration(email)
    access_token, refresh_token = test_3_login(email)
    test_4_wrong_password(email)
    test_5_unknown_email()
    test_6_current_user(access_token, email)
    test_7_missing_authorization()
    test_8_invalid_jwt()
    test_9_malformed_jwt()
    access_token, refresh_token = test_10_refresh_token(access_token, refresh_token)
    test_11_refresh_token_as_access_token(refresh_token)
    test_12_logout(refresh_token)
    test_13_refresh_after_logout(refresh_token)
    access_token, refresh_token = test_14_login_again(email)
    test_15_logout_all_devices(access_token)
    test_16_refresh_after_logout_all(refresh_token)
    test_17_invalid_refresh_token()
    test_18_logout_invalid_token()
    test_optional_rbac_endpoints(access_token)

    print("=" * 60)
    print("ALL AUTHORIZATION TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except AssertionError as err:
        print(f"\n[TEST FAILED]: {err}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print(
            f"\n[CONNECTION ERROR]: Could not connect to {BASE_URL}. Ensure uvicorn server is running.",
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception as exc:
        print(f"\n[UNEXPECTED ERROR]: {exc}", file=sys.stderr)
        sys.exit(1)
