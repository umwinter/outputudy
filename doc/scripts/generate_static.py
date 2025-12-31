import json
import urllib.request
import sys
import os

def generate_static_docs(backend_url, output_path):
    print(f"Fetching OpenAPI JSON from {backend_url}...")
    try:
        with urllib.request.urlopen(backend_url) as response:
            openapi_data = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching OpenAPI JSON: {e}")
        sys.exit(1)

    openapi_json_string = json.dumps(openapi_data)

    # Save openapi.json to src directory so MkDocs can include it
    # ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_path, "w") as f:
        f.write(openapi_json_string)
    print(f"Exported openapi.json to {output_path}")

if __name__ == "__main__":
    # Default values suitable for running inside doc container
    BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:8000/openapi.json")
    # Output directly to openapi.json in src
    OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "/docs/src/openapi.json")

    generate_static_docs(BACKEND_URL, OUTPUT_PATH)
