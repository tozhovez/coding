import os
import asyncio
from logging import Logger
from datetime import datetime
from injector import singleton, inject
from jobs.job_manager import JobManager
from core.consul_client import ConsulClient
from core.postgres_client import PostgresClient
from core.config_service import ConfigService
from services.sites_checker import SitesChecker

from status_code import StatusCode


@singleton
class SitesCheckerService:
    @inject
    def __init__(self,
                logger: Logger,
                job_manager: JobManager,
                consul_client: ConsulClient,
                postgres_client: PostgresClient,
                config_service: ConfigService,
                sites_checker_service: SitesChecker
                ):
        self.logger = logger
        self.job_manager = job_manager
        self.config_service = config_service
        self.postgres_client = postgres_client
        self.consul_client  = consul_client
        self.sites_checker_service = sites_checker_service

        self.service_start_time = None
        


    async def status(self):
        status_code = 0

        service_state = {
            'status_code': status_code,
        }

        return service_state


    async def kill(self):
        """
        Graceful exit
        """
        if self.job_manager:
            await self.job_manager.close()
        if self.sites_checker_service:
        #todo close
            pass


    async def _on_check(self):
        try:
            self.logger.info(f'SitesCheckerService Starting')
            await self.sites_checker_service.load()

        except Exception as ex:
            self.logger.error(
                'Unexpected error was raised while trying to log service state',
                exc_info=True
                )
            await self.kill()
        finally:
            self.logger.info(f'SitesCheckerService END')


    async def run(self):

        self.service_start_time = datetime.utcnow()

        try:
            self.consul_client.connect()
        except Exception as ex:
            self.logger.info('Cannot connect to infra services', exc_info=True)
            exit(1)

        # start background jobs
        self.job_manager.start()

        #self.job_manager.add_interval_job(self._on_check, self.config_service.job_interval)
        self.job_manager.run_once(self._on_check)

        self.logger.info('SitesCheckerService has started')
