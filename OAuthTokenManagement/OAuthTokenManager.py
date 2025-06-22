import requests
import time
import json

class AccessTokenManager:
    """
    Manages OAuth 2.0 access tokens for the Client Credentials flow with Azure AD.

    This class handles obtaining an initial access token and automatically refreshingwh
    it when it's near expiration, ensuring that API calls always use a valid token.
    """

    def __init__(self, tenant_id: str, client_id: str, client_secret: str, scope: str):
        """
        Initializes the AccessTokenManager.

        Args:
            tenant_id (str): Your Azure Active Directory tenant ID (GUID or domain name).
            client_id (str): The Application (client) ID of your registered Azure AD application.
            client_secret (str): The client secret for your Azure AD application.
            scope (str): The scope of the access token, e.g., "https://graph.microsoft.com/.default".
        """
        if not all([tenant_id, client_id, client_secret, scope]):
            raise ValueError("All parameters (tenant_id, client_id, client_secret, scope) must be provided.")

        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.token_endpoint = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"

        self._access_token = None
        self._expires_at = 0  # Unix timestamp when the token expires
        self._refresh_buffer_seconds = 300 # Refresh token 5 minutes before actual expiration

    def _get_new_access_token(self) -> str:
        """
        Internal method to request a new access token from Azure AD using the
        Client Credentials flow.

        Returns:
            str: The newly acquired access token.

        Raises:
            requests.exceptions.RequestException: If the HTTP request fails.
            ValueError: If the token response is malformed or indicates an error.
        """
        print("Attempting to get a new access token...")
        try:
            response = requests.post(
                self.token_endpoint,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "scope": self.scope
                },
                timeout=10 # Set a timeout for the request
            )
            response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

            token_data = response.json()

            if "access_token" not in token_data:
                raise ValueError(f"Access token not found in response: {token_data}")

            self._access_token = token_data["access_token"]
            # Calculate expiration time: current time + expires_in seconds
            self._expires_at = time.time() + token_data.get("expires_in", 3600)
            print("Access token obtained successfully.")
            return self._access_token

        except requests.exceptions.RequestException as e:
            print(f"Error making request to token endpoint: {e}")
            raise
        except json.JSONDecodeError:
            print(f"Error decoding JSON response from token endpoint: {response.text}")
            raise ValueError("Invalid JSON response from token endpoint.")
        except ValueError as e:
            print(f"Error in token response data: {e}")
            raise

    def get_access_token(self) -> str:
        """
        Provides a valid access token. If the current token is expired or
        near expiration, it automatically requests a new one.

        Returns:
            str: A valid access token.
        """
        # Check if the current token is valid or needs refreshing
        # We refresh if the current time is beyond (expiration time - buffer)
        if not self._access_token or (time.time() + self._refresh_buffer_seconds) >= self._expires_at:
            print("Access token expired or nearing expiration. Refreshing...")
            self._get_new_access_token()
        return self._access_token

# --- Example Usage ---
if __name__ == "__main__":
    # IMPORTANT: Replace these placeholders with your actual Azure AD details.
    # NEVER hardcode sensitive credentials in production code.
    # Use environment variables or a secure configuration management system.
    YOUR_TENANT_ID = "YOUR_AZURE_AD_TENANT_ID" # e.g., "yourcompany.onmicrosoft.com" or a GUID
    YOUR_CLIENT_ID = "YOUR_AZURE_AD_CLIENT_ID"
    YOUR_CLIENT_SECRET = "YOUR_AZURE_AD_CLIENT_SECRET"
    YOUR_SCOPE = "https://graph.microsoft.com/.default" # Or other desired scope, e.g., "api://yourappid/.default"

    # --- Step 1: Initialize the token manager ---
    try:
        token_manager = AccessTokenManager(
            tenant_id=YOUR_TENANT_ID,
            client_id=YOUR_CLIENT_ID,
            client_secret=YOUR_CLIENT_SECRET,
            scope=YOUR_SCOPE
        )
    except ValueError as e:
        print(f"Initialization failed: {e}")
        print("Please ensure all Azure AD configuration details are provided.")
        exit() # Exit if configuration is missing

    # --- Step 2: Get the first token ---
    # The first call will automatically trigger token acquisition
    try:
        current_token = token_manager.get_access_token()
        print(f"\nInitial Access Token (first 20 chars): {current_token[:20]}...")
        print(f"Token expires in approx. {round(token_manager._expires_at - time.time())} seconds.")

        # --- Simulate making an API call with the token ---
        print("\nSimulating an API call with the current token...")
        # In a real scenario, you'd use this token in an 'Authorization: Bearer <token>' header
        # For example:
        # headers = {"Authorization": f"Bearer {current_token}"}
        # api_response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)
        # print(api_response.json())

        # --- Simulate time passing and token expiring (for testing purposes) ---
        print("\nSimulating time passing to force token refresh...")
        # Artificially set the expiration time close to now for demonstration
        token_manager._expires_at = time.time() + (token_manager._refresh_buffer_seconds / 2) # e.g., 2.5 minutes from now

        print(f"Artificially set token to expire in approx. {round(token_manager._expires_at - time.time())} seconds.")
        time.sleep(token_manager._refresh_buffer_seconds / 2 + 10) # Wait past the refresh buffer + a bit more

        # --- Step 3: Get token again, triggering a refresh ---
        print("\nRequesting token again after simulated time passage...")
        refreshed_token = token_manager.get_access_token()
        print(f"Refreshed Access Token (first 20 chars): {refreshed_token[:20]}...")
        print(f"Token expires in approx. {round(token_manager._expires_at - time.time())} seconds.")

        # Verify that the token actually refreshed (it should be different from the initial token)
        if current_token != refreshed_token:
            print("\nToken successfully refreshed! The new token is different from the original.")
        else:
            print("\nToken did NOT refresh (this might indicate an issue with the refresh logic or very fast execution).")

    except requests.exceptions.RequestException as e:
        print(f"\nAn error occurred during token acquisition or simulation: {e}")
        print("Please check your network connection and Azure AD configuration (client_id, client_secret, tenant_id, scope).")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

