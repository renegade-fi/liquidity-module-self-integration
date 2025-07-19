from dataclasses import dataclass
from importlib.metadata import version
from typing import Optional

from httpx import Headers, Response

from .http import RelayerHttpClient
from .types import (
    ExternalMatchRequest,
    ExternalMatchResponse,
    ExternalOrder,
)

ARBITRUM_SEPOLIA_BASE_URL = "https://arbitrum-sepolia.auth-server.renegade.fi"
ARBITRUM_ONE_BASE_URL = "https://arbitrum-one.auth-server.renegade.fi"
BASE_SEPOLIA_BASE_URL = "https://base-sepolia.auth-server.renegade.fi"
BASE_MAINNET_BASE_URL = "https://base-mainnet.auth-server.renegade.fi"

RENEGADE_API_KEY_HEADER = "x-renegade-api-key"
RENEGADE_SDK_VERSION_HEADER = "x-renegade-sdk-version"

REQUEST_EXTERNAL_MATCH_ROUTE = "/v0/matching-engine/request-external-match"

DISABLE_GAS_SPONSORSHIP_QUERY_PARAM = "disable_gas_sponsorship"
GAS_REFUND_ADDRESS_QUERY_PARAM = "refund_address"

"""
Helpers
"""


def _get_sdk_version() -> str:
    """Get the SDK version, falling back to the hardcoded version if not installed.

    Returns:
        The SDK version string prefixed with "python-v"
    """
    try:
        sdk_version = version("gluex-liquidity-module-v{sdk_version}")
    except Exception:
        sdk_version = "unknown"
    return f"python-v{sdk_version}"


"""
Types
"""


class ExternalMatchClientError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


@dataclass
class ExternalMatchOptions:
    do_gas_estimation: bool = False
    receiver_address: Optional[str] = None
    request_gas_sponsorship: bool = False
    gas_refund_address: Optional[str] = None
    updated_order: Optional[ExternalOrder] = None

    @classmethod
    def new(cls) -> "ExternalMatchOptions":
        return cls()

    def with_gas_estimation(self, do_gas_estimation: bool) -> "ExternalMatchOptions":
        self.do_gas_estimation = do_gas_estimation
        return self

    def with_receiver_address(self, receiver_address: str) -> "ExternalMatchOptions":
        self.receiver_address = receiver_address
        return self

    def with_gas_sponsorship(
        self, request_gas_sponsorship: bool, gas_refund_address: Optional[str] = None
    ) -> "ExternalMatchOptions":
        self.request_gas_sponsorship = request_gas_sponsorship
        self.gas_refund_address = gas_refund_address
        return self

    def with_updated_order(
        self, updated_order: ExternalOrder
    ) -> "ExternalMatchOptions":
        self.updated_order = updated_order
        return self

    def build_request_path(self) -> str:
        """
        Builds the path at which the request will be sent, with query params
        """
        disable_sponsorship_str = str(not self.request_gas_sponsorship).lower()
        path = f"{REQUEST_EXTERNAL_MATCH_ROUTE}?{DISABLE_GAS_SPONSORSHIP_QUERY_PARAM}={disable_sponsorship_str}"
        if self.gas_refund_address:
            path += f"&{GAS_REFUND_ADDRESS_QUERY_PARAM}={self.gas_refund_address}"

        return path


"""
Client
"""


class ExternalMatchClient:
    """Client for interacting with the Renegade external matching API.

    This client handles authentication and provides methods for requesting quotes,
    assembling matches, and executing trades.
    """

    def __init__(self, api_key: str, api_secret: str, base_url: str):
        """Initialize a new ExternalMatchClient.

        Args:
            api_key: The API key for authentication
            api_secret: The API secret for request signing
            base_url: The base URL of the Renegade API
        """
        self.api_key = api_key
        self.http_client = RelayerHttpClient(base_url, api_secret)

    @classmethod
    def new_arbitrum_sepolia_client(
        cls, api_key: str, api_secret: str
    ) -> "ExternalMatchClient":
        """Create a new client configured for the Arbitrum Sepolia testnet.

        Args:
            api_key: The API key for authentication
            api_secret: The API secret for request signing

        Returns:
            A new ExternalMatchClient configured for Arbitrum Sepolia
        """
        return cls(api_key, api_secret, ARBITRUM_SEPOLIA_BASE_URL)

    @classmethod
    def new_base_sepolia_client(
        cls, api_key: str, api_secret: str
    ) -> "ExternalMatchClient":
        """Create a new client configured for Base Sepolia testnet.

        Args:
            api_key: The API key for authentication
            api_secret: The API secret for request signing

        Returns:
            A new ExternalMatchClient configured for Base Sepolia
        """
        return cls(api_key, api_secret, BASE_SEPOLIA_BASE_URL)

    @classmethod
    def new_arbitrum_one_client(
        cls, api_key: str, api_secret: str
    ) -> "ExternalMatchClient":
        """Create a new client configured for Arbitrum One.

        Args:
            api_key: The API key for authentication
            api_secret: The API secret for request signing

        Returns:
            A new ExternalMatchClient configured for Arbitrum One
        """
        return cls(api_key, api_secret, ARBITRUM_ONE_BASE_URL)

    @classmethod
    def new_base_mainnet_client(
        cls, api_key: str, api_secret: str
    ) -> "ExternalMatchClient":
        """Create a new client configured for Base mainnet.

        Args:
            api_key: The API key for authentication
            api_secret: The API secret for request signing

        Returns:
            A new ExternalMatchClient configured for Base mainnet
        """
        return cls(api_key, api_secret, BASE_MAINNET_BASE_URL)

    async def request_external_match(
        self, order: ExternalOrder
    ) -> ExternalMatchResponse:
        """Request a quote for the given order with the default options.

        Args:
            order: The order to request a quote for

        Returns:
            A signed quote if one is available, None otherwise

        Raises:
            ExternalMatchClientError: If the request fails
        """
        options = ExternalMatchOptions.new()
        options.with_gas_sponsorship(request_gas_sponsorship=True)
        return await self.request_external_match_with_options(order, options)

    async def request_external_match_with_options(
        self, order: ExternalOrder, options: ExternalMatchOptions
    ) -> ExternalMatchResponse:
        """Request a quote for the given order.

        Args:
            order: The order to request a quote for

        Returns:
            An ExternalMatchResponse containing the quote and settlement tx data if available, None otherwise

        Raises:
            ExternalMatchClientError: If the request fails
        """
        request = ExternalMatchRequest(
            do_gas_estimation=options.do_gas_estimation,
            external_order=order,
            receiver_address=options.receiver_address,
        )

        path = options.build_request_path()
        headers = self._get_headers()
        body = request.model_dump()
        response = await self.http_client.post_with_headers(path, body, headers)
        match_resp = self._handle_optional_response(response)

        if match_resp is None:
            return None

        match_resp = ExternalMatchResponse(**match_resp)
        return match_resp

    def _get_headers(self) -> Headers:
        """Get the headers required for API requests.

        Returns:
            Headers containing the API key and SDK version
        """
        headers = Headers()
        headers[RENEGADE_API_KEY_HEADER] = self.api_key
        headers[RENEGADE_SDK_VERSION_HEADER] = _get_sdk_version()
        return headers

    def _handle_optional_response(self, response: Response) -> Optional[dict]:
        """Handle an API response that may be empty.

        Args:
            response: The API response to handle

        Returns:
            The response data if present, None for 204 responses

        Raises:
            ExternalMatchClientError: If the response indicates an error
        """
        if response.status_code == 204:  # NO_CONTENT
            return None
        elif response.status_code == 200:  # OK
            return response.json()
        else:
            raise ExternalMatchClientError(
                response.text, status_code=response.status_code
            )
