from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

# Setup template environment
# Assuming templates are at backend/app/templates
TEMPLATE_DIR = Path(__file__).parent.parent.parent / "templates"

env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(["html", "xml"]),
)


def render_email_template(template_name: str, context: dict) -> str:
    template = env.get_template(template_name)
    return template.render(context)
