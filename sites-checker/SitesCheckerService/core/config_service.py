
import os
from injector import singleton, inject
from consul_client import ConsulClient


@singleton
class ConfigService:
    """config parameters"""
    @inject
    def __init__(self, consul_client: ConsulClient):
        self.consul_client = consul_client

        self.postgres_url = consul_client.get('postgres_url', prefix='shared')

        self.job_interval = self.consul_client.get(
            'job_interval', prefix='sites-checker-service')

        self.data_src_folder = self.consul_client.get(
            'data_src_folfer', prefix='sites-checker-service')

        self.data_src_url = self.consul_client.get(
            'data_src_url', prefix='sites-checker-service')

        self.virus_total_src_folfer = self.consul_client.get(
            'virus_total_src_folfer', prefix='sites-checker-service')

        self.virus_total_src_url = self.consul_client.get(
            'virus_total_src_url', prefix='sites-checker-service')

        #load in env : production , local ant other
        self.run_env = os.environ['RUNS_IN_DOCKER'] or -1
