import json
import os

from app.main import app


def export_openapi() -> None:
    # Use FastAPI's utility to get the JSON schema
    openapi_schema = app.openapi()

    # Target path relative to project root (or as specified by env)
    output_path = os.environ.get("OPENAPI_OUTPUT_PATH", "openapi.json")

    with open(output_path, "w") as f:
        json.dump(openapi_schema, f, indent=2)

    print(f"✅ OpenAPI schema exported to {output_path}")


if __name__ == "__main__":
    export_openapi()
