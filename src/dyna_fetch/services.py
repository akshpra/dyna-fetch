from typing import Any, Literal, Self
from urllib.parse import urlencode, urljoin

import httpx
import msgspec

from loguru import logger


class Service:
    """Web service for querying Dynamics Business Central OData API."""

    def __init__(
        self, base_url: str, service_name: str, client: httpx.Client, model: type[msgspec.Struct]
    ) -> None:
        """
        Initialize a Service instance for querying the given OData service.

        Args:
            base_url (str): The base URL of the Dynamics Business Central OData API.
            service_name (str): The name of the OData service to query.
            client (httpx.Client): The HTTP client to use for making requests.
            model (msgspec.Struct): The msgspec struct class that defines the expected
                structure of the response.

        Returns:
            Service: A Service instance for querying the specified OData service.

        """
        self.base_url = base_url
        self.service_name = service_name
        self.client = client
        self.model = model

        # Initialize with $select and $count parameter that includes all fields from the model
        self.params: dict[str, int | float | str] = {
            "$select": self._get_select_fields(),
            "$count": "true",
        }

    def _get_select_fields(self) -> str:
        """
        Get the select fields from the model.

        Returns:
            str: The select fields as a comma-separated string.

        """
        field_names = [field.encode_name for field in msgspec.structs.fields(self.model)]
        return ",".join(field_names)

    def _set_params(self, param_key: str, param_value: int | float | str) -> None:
        """
        Set a parameter in the request. If the parameter is already set, raise an error.

        Args:
            param_key (str): The key of the parameter to set.
            param_value (int | float | str): The value of the parameter to set.

        Raises:
            ValueError: If the parameter is already set.

        """
        if param_key in self.params:
            raise ValueError(f"Parameter {param_key} is already set.")
        self.params[param_key] = param_value

    def _create_response_struct(self) -> type[msgspec.Struct]:
        """
        Create a msgspec struct class that defines the expected structure of the response.

        Returns:
            msgspec.Struct: The msgspec struct class that defines the expected
                structure of the response.

        """
        model = self.model

        class Response(msgspec.Struct, kw_only=True):
            """Response struct for querying the Dynamics Business Central OData API."""

            value: list[model]  # type: ignore
            count: int | None = msgspec.field(name="@odata.count", default=None)
            next_link: str | None = msgspec.field(name="@odata.nextLink", default=None)

            def to_dict(self) -> list[dict[str, Any]]:
                """Convert the response to a list of dictionaries."""
                return [msgspec.structs.asdict(item) for item in self.value]

        return Response

    def _build_url(self) -> str:
        """
        Build the URL for the request. Includes the base URL, service name, and parameters.

        Returns:
            str: The URL for the request.

        """
        url = urljoin(self.base_url + "/", self.service_name)
        query_string = urlencode(self.params)
        return f"{url}?{query_string}"

    def filter(self, value: str) -> Self:
        """
        Set the filter expression for the request.

        Args:
            value (str): The filter expression to apply to the request.

        Returns:
            Service: The Service instance with the filter expression set.

        """
        self._set_params("$filter", value)
        return self

    def top(self, value: int) -> Self:
        """
        Set the top parameter for the request.

        Args:
            value (int): The number of records to return.

        Returns:
            Service: The Service instance with the top parameter set.

        """
        self._set_params("$top", value)
        return self

    def skip(self, value: int) -> Self:
        """
        Set the skip parameter for the request.

        Args:
            value (int): The number of records to skip.

        Returns:
            Service: The Service instance with the skip parameter set.

        """
        self._set_params("$skip", value)
        return self

    def order_by(self, field: str, ordering: Literal["asc", "desc"] = "asc") -> Self:
        """
        Set the order by parameter for the request.

        Args:
            field (str): The field to order by.
            ordering (Literal["asc", "desc"]): The ordering to use.

        Returns:
            Service: The Service instance with the order by parameter set.

        """
        self._set_params("$orderby", f"{field} {ordering}")
        return self

    @logger.catch
    def get(self) -> list[dict[str, Any]]:
        """
        Fetch data from the Dynamics Business Central OData API.

        Returns:
            list[dict[str, Any]]: The data from the Dynamics Business Central OData API.

        """
        response_struct = self._create_response_struct()
        url = self._build_url()

        data: list[dict[str, Any]] = []

        while url:
            try:
                logger.debug(f"Fetching data from {url}")
                response = self.client.get(url)
                response.raise_for_status()
                validated_data = msgspec.json.decode(response.content, type=response_struct)
                data.extend(validated_data.to_dict())  # type: ignore
                url = validated_data.next_link  # type: ignore
                logger.info(
                    f"Loaded {len(data)} of {validated_data.count} records from {self.service_name}"  # type: ignore
                )
            except httpx.HTTPError as e:
                logger.error(f"Error fetching data from {url}: {e}")
                raise

        return data

    def fetch(self) -> list[dict[str, Any]]:
        """
        Fetch data from the Dynamics Business Central OData API.

        Returns:
            Any: The data from the Dynamics Business Central OData API.

        """
        return self.get()

    def __str__(self) -> str:
        """Return a string representation of the Service instance."""
        return f"Service(base_url={self.base_url}, service_name={self.service_name})"

    def __repr__(self) -> str:
        """Return a string representation of the Service instance."""
        return self.__str__()
