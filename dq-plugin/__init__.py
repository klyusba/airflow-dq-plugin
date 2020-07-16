from airflow.plugins_manager import AirflowPlugin

from demo_plugin.blueprints import BLUEPRINTS
from demo_plugin.hooks import HOOKS
from demo_plugin.menu_links import MENU_LINKS
from demo_plugin.operators import OPERATORS
from demo_plugin.sensors import SENSORS
from demo_plugin.views import VIEWS


class AirflowPluginDemo(AirflowPlugin):
    name = 'dq'
    operators = OPERATORS + SENSORS
    flask_blueprints = BLUEPRINTS
    hooks = HOOKS
    executors = []
    macros = []
    admin_views = VIEWS
    menu_links = MENU_LINKS
