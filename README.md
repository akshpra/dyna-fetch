# DynaFetch

A Python library for querying the Dynamics Business Central OData API with a clean, fluent interface.

## Features

- Simple, chainable query building
- Type-safe responses with automatic validation via msgspec
- Built-in pagination handling
- Fluent filtering syntax
- Automatic field selection based on your data models
- Comprehensive logging
- HTTP request handling with timeout management

## Installation

```bash
pip install dyna-fetch
```

## Requirements

- Python 3.12+
- httpx
- msgspec
- loguru

## Quick Start

```python
from datetime import date
import msgspec
from dyna_fetch import DynaFetchClient, Q

# Define your data model
class ItemLedgerEntry(msgspec.Struct, kw_only=True):
    """Model for Item Ledger Entry."""
    entry_type: str = msgspec.field(name="Entry_Type")
    posting_date: date = msgspec.field(name="Posting_Date")
    item_no: str = msgspec.field(name="Item_No")
    quantity: float = msgspec.field(name="Quantity")
    amount: float = msgspec.field(name="Cost_Amount_Actual")

    def __post_init__(self) -> None:
        """Post initialization cleanup."""
        self.quantity = round(self.quantity, 4)
        self.amount = round(self.amount, 2)

# Initialize the client
base_url = "http://odata-api.com/bc-service/odatav4/Company('COMPANY')"
auth = ("username", "password")
client = DynaFetchClient(base_url=base_url, auth=auth)

# Build a complex filter
filter_expression = Q.and_group(
    Q.or_group(Q.eq("Entry_Type", "Sale"), Q.eq("Entry_Type", "Purchase")),
    Q.or_group(Q.eq("Item_No", "FIL-179"), Q.eq("Item_No", "CAR-206")),
)

# Execute the query with chained operations
items = (
    client.query(service_name="ksppl_item_ledger_entries", model=ItemLedgerEntry)
    .filter(filter_expression)
    .order_by(field="Posting_Date", ordering="desc")
    .top(10)
    .skip(10)
    .fetch()
)

# Use the results
for item in items:
    print(f"{item['item_no']}: {item['quantity']} units, ${item['amount']}")
```

## Key Components

### DynaFetchClient

The main client that initializes connections to the Dynamics Business Central OData API.

```python
client = DynaFetchClient(
    base_url="http://odata-api.com/bc-service/odatav4/Company('COMPANY')",
    auth=("username", "password"),  # Optional: Basic auth credentials
    timeout=60  # Optional: Request timeout in seconds (default: 60)
)
```

### Service

The Service class handles specific OData service endpoints. You typically don't instantiate this directly, but through the `client.query()` method.

```python
service = client.query(
    service_name="ksppl_item_ledger_entries",  # The OData service to query
    model=ItemLedgerEntry  # Your msgspec Struct model
)
```

### Filtering with Q

The `Q` class provides a fluent interface for building OData filter expressions:

```python
from dyna_fetch import Q

# Basic filters
Q.eq("field_name", "value")      # field_name eq 'value'
Q.ne("field_name", 123)          # field_name ne 123
Q.lt("field_name", 50.5)         # field_name lt 50.5
Q.gt("field_name", 20)           # field_name gt 20
Q.le("field_name", 100)          # field_name le 100
Q.ge("field_name", 0)            # field_name ge 0

# String functions
Q.contains("field_name", "substring")      # contains(field_name, 'substring')
Q.startswith("field_name", "prefix")       # startswith(field_name, 'prefix')
Q.endswith("field_name", "suffix")         # endswith(field_name, 'suffix')

# Logical groups
Q.and_group(                               # (condition1 and condition2 and condition3)
    Q.eq("field1", "value1"),
    Q.gt("field2", 100),
    Q.contains("field3", "search")
)

Q.or_group(                                # (condition1 or condition2 or condition3)
    Q.eq("field1", "value1"),
    Q.eq("field1", "value2"),
    Q.eq("field1", "value3")
)

# Complex nested filters
complex_filter = Q.and_group(
    Q.or_group(
        Q.eq("Status", "Active"),
        Q.eq("Status", "Pending")
    ),
    Q.gt("Amount", 1000),
    Q.lt("Date", date(2023, 12, 31))
)
```

### Data Models with msgspec

Define your data models using `msgspec.Struct` with field mappings to match the OData response:

```python
import msgspec
from datetime import date

class Customer(msgspec.Struct, kw_only=True):
    customer_id: str = msgspec.field(name="No")
    name: str = msgspec.field(name="Name")
    email: str = msgspec.field(name="E_Mail")
    phone: str | None = msgspec.field(name="Phone_No", default=None)
    created_date: date = msgspec.field(name="Creation_Date")
    credit_limit: float = msgspec.field(name="Credit_Limit_LCY")

    def __post_init__(self) -> None:
        """Optional post-processing of fields."""
        self.customer_id = self.customer_id.strip()
        self.credit_limit = round(self.credit_limit, 2)
```

## Query Methods

Chain these methods to build your query:

```python
# Basic query
result = client.query("customers", CustomerModel).fetch()

# With filter
result = client.query("customers", CustomerModel).filter(Q.eq("Active", True)).fetch()

# With ordering
result = client.query("customers", CustomerModel).order_by("Name", "asc").fetch()

# With pagination
result = client.query("customers", CustomerModel).top(50).skip(100).fetch()

# Combined operations
result = (
    client.query("customers", CustomerModel)
    .filter(Q.gt("Credit_Limit_LCY", 10000))
    .order_by("Name")
    .top(25)
    .fetch()
)
```

## Advanced Features

### Automatic Field Selection

DynaFetch automatically generates the `$select` parameter based on your model's field definitions, optimizing the response payload.

### Pagination Handling

The library automatically handles pagination for you. When a response includes a `@odata.nextLink`, DynaFetch will follow it and combine all results before returning.

### Comprehensive Logging

DynaFetch uses `loguru` for logging, providing detailed information about API requests and responses:

```python
from loguru import logger

# Configure loguru as needed
logger.add("dyna_fetch.log", rotation="10 MB")
```

## Best Practices

1. **Define Clear Models**: Create typed models with appropriate field mappings that match your Dynamics Business Central fields.

2. **Use Post-Processing**: Leverage `__post_init__` to clean or transform data after it's received.

3. **Optimize Query Size**: Use filters, skip, and top methods to limit the amount of data transferred.

4. **Handle Exceptions**: Wrap your API calls in try/except blocks to handle potential HTTP or validation errors.

```python
from dyna_fetch import DynaFetchClient
import httpx

try:
    client = DynaFetchClient(base_url="https://api.example.com")
    data = client.query("items", ItemModel).fetch()
except httpx.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
```
