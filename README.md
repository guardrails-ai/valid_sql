# Overview

| Developed by | Guardrails AI |
| --- | --- |
| Date of development | Feb 15, 2024 |
| Validator type | Format |
| Blog |  |
| License | Apache 2 |
| Input/Output | Output |

# Description

This validator checks if a string follows valid SQL code. In order to do this, it expects either a `conn` string or a `schema` file. It checks the validity of generated SQL by performing the following steps:

1. If given a connection string, it connects to the DB instance.
2. Alternatively, if given a schema, it creates a local instance of the database based on the schema and connects to the local DB.
3. If neither a connection string nor schema is provided, then SQL validation is performed using `sqlvalidator` package.
4. In order to validate any generated LLM string representing a SQL statement, that statement is executed against the connected DB. If the statement runs without raising an exception, then the validator passes.

# Installation

```bash
$ guardrails hub install hub://guardrails/valid_sql
```

# Usage Examples

## Validating string output via Python

In this example, we validate a generated SQL code by providing it with a schema file.

```python
# Import Guard and Validator
from guardrails.hub import ValidSQL
from guardrails import Guard

with open("schema.sql", "w") as f:
		f.write("""
CREATE TABLE IF NOT EXISTS employees (
    id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);
"""
		)

# Initialize Validator
val = ValidSQL(
    schema_file="schema.sql",
    conn="sqlite://",
)

# Setup Guard
guard = Guard.from_string(
    validators=[val, ...],
)

guard.parse("select name from employees;")  # Validator passes
guard.parse("select name, fro employees")  # Validator fails
```

## Validating JSON output via Python

In this example, we apply the validator to a string field of a JSON object.

```python
# Import Guard and Validator
from pydantic import BaseModel
from guardrails.hub import ValidSQL
from guardrails import Guard

with open("schema.sql", "w") as f:
		f.write("""
CREATE TABLE IF NOT EXISTS employees (
    id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);
"""
		)

# Initialize Validator
val = ValidSQL(
    schema_file="schema.sql",
    conn="sqlite://",
)

# Create Pydantic BaseModel
class SQLCode(BaseModel):
    code: str = Field(
        description="SQL code for query", validators=[val]
    )

# Create a Guard to check for valid Pydantic output
guard = Guard.from_pydantic(output_class=SQLCode)

# Run LLM output generating JSON through guard
guard.parse("""
{
    "code": "select name from employees;"
}
""")
```


# API Reference

`__init__`

- `conn`: The connection string to connect to a sql schema. E.g. `sqlite://`
- `schema`: The `.sql` file representing the DB schema.
- `on_fail`: The policy to enact when a validator fails.
