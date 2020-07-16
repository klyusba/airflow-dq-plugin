from flask import Blueprint

PluginBlueprint = Blueprint(
    'demo_plugin', __name__,
    template_folder='../templates',
    static_folder='../static',
    static_url_path='/static/demo_plugin/'
)

BLUEPRINTS = [
    PluginBlueprint,
]
