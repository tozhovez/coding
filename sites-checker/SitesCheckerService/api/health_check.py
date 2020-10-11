from datetime import datetime
from sanic import Blueprint
from sanic.response import json
from injector import inject, singleton
from logging import Logger
from datetime import datetime
import time

@singleton
class HealthCheckController:
    @inject
    def __init__(self, logger: Logger):
        self.logger = logger


    async def check_health(self, request):
        """ check_health """
        # get current state

        # write response

        return 200



# ! TEMPORARY
def create_health_check_controller(health_check_controller: HealthCheckController, app):
    health_check_bp = Blueprint('health_check')

    @health_check_bp.route('/health_check')
    async def decorated_get_health_check(request):
        return await health_check_controller.check_health(request)
    app.blueprint(health_check_bp)
