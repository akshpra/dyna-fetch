import httpx
import msgspec

from loguru import logger

from .services import Service


class DynaFetchClient:
    """Client for querying Dynamics Business Central OData API."""

    def __init__(
        self, base_url: str, auth: tuple[str, str] | None = None, timeout: int = 60
    ) -> None:
        """
        Initialize a DynaFetchClient instance.

        Args:
            base_url (str): The base URL of the Dynamics Business Central OData API.
            auth (tuple[str, str] | None, optional): The authentication tuple containing
                the username and password to use for Basic Auth. Defaults to None.
            timeout (int, optional): The timeout in seconds to use for requests.
                Defaults to 60.

        """
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(auth=auth, timeout=timeout)
        logger.debug(f"New DynaFetchClient created for {base_url}")

    def query(self, service_name: str, model: type[msgspec.Struct]) -> Service:
        """
        Initialize a Service instance for querying the given OData service.

        Args:
            service_name (str): The name of the OData service to query.
            model (type[T]): The msgspec struct class that defines the expected
                structure of the response.

        Returns:
            Service: A Service instance for querying the specified OData service.

        """
        service_name = service_name.strip("/")
        return Service(
            base_url=self.base_url, service_name=service_name, client=self.client, model=model
        )

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return f"DynaFetchClient({self.base_url})"

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return self.__str__()
