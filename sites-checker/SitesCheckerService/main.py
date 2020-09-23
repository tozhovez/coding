
import signal
import asyncio
import logging
from sanic import Sanic
from sanic_cors import CORS
from injector import Injector
from core.core_module import CoreModule

from sites_checker_service  import SitesCheckerService
from api.health_check import HealthCheckController, create_health_check_controller

app = None
sch_service = None


async def main(ioc_container):
    global sch_service

    # set a fatal exception handler
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(fatal_exception_handler)

    # start service
    sch_service = ioc_container.get(SitesCheckerService)
    await sch_service.run()



def fatal_exception_handler(loop, context):
    global sch_service

    logger = logging.getLogger('SitesCheckerService')

    exception = context.get('exception')
    logger.error(
        'Fatal error in SitesCheckerService, closing program..',
        extra={"exception": str(exception)}
        )

    loop.create_task(sch_service.kill())
    app.stop()

    exit(1)


async def shutdown(signal, loop):
    global sch_service

    logger = logging.getLogger('SitesCheckerService')
    logger.info('bye')

    await sch_service.kill()


if __name__ == "__main__":

    app = Sanic(configure_logging=False)
    CORS(app, automatic_options=True)

    ioc_container = Injector(modules=[CoreModule])
    # catch signals
    app.register_listener(shutdown, 'before_server_stop')
    #
    # create controllers
    #
    # health check
    #health_check_controller = ioc_container.get(HealthCheckController)
    create_health_check_controller(health_check_controller, app)

    app.add_task(main(ioc_container))
    app.run(host="0.0.0.0", port=5021)
