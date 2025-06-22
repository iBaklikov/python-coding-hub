import requests
import time
import json
import os

class AccessTokenManagerWithRefresh:
    def __init__(self, tenant_id: str, client_id: str, client_secret: str, scope: str, token_file: str = "token.json"):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.token_file = token_file
        self.token_endpoint = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"

        self._access_token = None
        self._refresh_token = None
        self._expires_at = 0
        self._refresh_buffer_seconds = 300

        self._load_tokens_from_file()

    def _load_tokens_from_file(self):
        if os.path.exists(self.token_file):
            try:
                with open(self.token_file, "r") as f:
                    data = json.load(f)
                    self._access_token = data.get("access_token")
                    self._refresh_token = data.get("refresh_token")
                    self._expires_at = data.get("expires_at", 0)
            except Exception as e:
                print(f"Failed to load token file: {e}")

    def _save_tokens_to_file(self):
        try:
            with open(self.token_file, "w") as f:
                json.dump({
                    "access_token": self._access_token,
                    "refresh_token": self._refresh_token,
                    "expires_at": self._expires_at
                }, f, indent=2)
        except Exception as e:
            print(f"Failed to save tokens: {e}")

    def _refresh_access_token(self):
        print("Using refresh token to get new access token...")
        try:
            response = requests.post(
                self.token_endpoint,
                data={
                    "grant_type": "refresh_token",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "scope": self.scope,
                    "refresh_token": self._refresh_token
                },
                timeout=10
            )
            response.raise_for_status()
            token_data = response.json()

            self._access_token = token_data["access_token"]
            self._refresh_token = token_data.get("refresh_token", self._refresh_token)
            self._expires_at = time.time() + token_data.get("expires_in", 3600)

            self._save_tokens_to_file()
            print("Token refreshed and saved successfully.")
        except requests.RequestException as e:
            print(f"Request error: {e}")
            raise
        except Exception as e:
            print(f"Token refresh failed: {e}")
            raise

    def _get_new_token_with_client_credentials(self):
        print("No refresh token found. Using client_credentials flow...")
        try:
            response = requests.post(
                self.token_endpoint,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "scope": self.scope
                },
                timeout=10
            )
            response.raise_for_status()
            token_data = response.json()
            self._access_token = token_data["access_token"]
            self._refresh_token = token_data.get("refresh_token", None)
            self._expires_at = time.time() + token_data.get("expires_in", 3600)

            self._save_tokens_to_file()
            print("Token acquired using client credentials and saved.")
        except Exception as e:
            print(f"Failed to get token using client credentials: {e}")
            raise

    def get_access_token(self) -> str:
        if not self._access_token or (time.time() + self._refresh_buffer_seconds) >= self._expires_at:
            if self._refresh_token:
                self._refresh_access_token()
            else:
                self._get_new_token_with_client_credentials()
        return self._access_token


if __name__ == "__main__":
    token_manager = AccessTokenManagerWithRefresh(
        tenant_id="YOUR_TENANT_ID",
        client_id="YOUR_CLIENT_ID",
        client_secret="YOUR_CLIENT_SECRET",
        scope="https://graph.microsoft.com/.default",
        token_file="token.json"
    )

    token = token_manager.get_access_token()
    print("Access Token (first 20 chars):", token[:20])

