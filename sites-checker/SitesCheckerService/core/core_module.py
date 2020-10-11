
import os
import logging
from logging import Logger
from injector import provider, singleton, Module
import pyfortified_logging
from pyfortified_logging import get_logger, LoggingFormat, LoggingOutput
from consul_client import ConsulClient
from postgres_client import PostgresClient
from config_service import ConfigService


class CoreModule(Module):
    """config modules"""

    @singleton
    @provider
    def provide_consul_client(self) -> ConsulClient:
        """innit consul client"""
        return ConsulClient(
            host=os.getenv('CONSUL_HOST', '127.0.0.1'),
            prefix='sites-checker-service',
        )

    @singleton
    @provider
    def provide_postgres_client(self,
                                conf_service: ConfigService
                                ) -> PostgresClient:
        """innit Postgres client"""
        # TODO: check asyncio support
        # await postgres_client.connect()
        return PostgresClient(dsn=conf_service.postgres_url)

    @singleton
    @provider
    def provide_logger(self) -> Logger:
        """innit logger"""
        return get_logger(
            logger_name='SitesCheckerService',
            logger_format=LoggingFormat.JSON,
            logger_level=logging.INFO,
            logger_output=LoggingOutput.STDOUT,
        )
