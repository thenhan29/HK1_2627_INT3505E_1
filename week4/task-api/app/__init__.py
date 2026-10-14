"""Create and configure the Flask application."""

from pathlib import Path

import yaml
from flask import Flask, jsonify, render_template_string, request

from .routes import api_bp

OPENAPI_SPEC_PATH = Path(__file__).resolve().parent.parent / "bundled-openapi.yaml"
SWAGGER_UI_PAGE = """<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Task API - Swagger UI</title>
        <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
        <script>
            SwaggerUIBundle({
                url: {{ spec_url|tojson }},
                dom_id: '#swagger-ui',
                tryItOutEnabled: true,
                presets: [SwaggerUIBundle.presets.apis],
                layout: 'BaseLayout'
            });
        </script>
    </body>
</html>"""


def create_app(test_config=None):
    """Application factory used by the server and tests."""
    app = Flask(__name__)

    if test_config:
        app.config.update(test_config)

    app.register_blueprint(api_bp)

    @app.get("/openapi.json")
    def openapi_json():
        with OPENAPI_SPEC_PATH.open(encoding="utf-8") as spec_file:
            spec = yaml.safe_load(spec_file)
        spec["servers"] = [{"url": request.host_url.rstrip("/")}]
        return jsonify(spec)

    @app.get("/docs")
    def swagger_ui():
        return render_template_string(
            SWAGGER_UI_PAGE,
            spec_url=f"{request.script_root}/openapi.json",
        )

    return app
