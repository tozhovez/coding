

import os
import yaml
import subprocess
from PyInquirer import prompt, Separator
from screeninfo import get_monitors
from consul_client import ConsulClient


CORE_SERVICES = [
    {
        'name': 'Sites Checker Service',
        'value': {
            'name': 'sites-checker-service',
            'service_build_directory': 'SitesCheckerService',
            'working_directory': '.'
        }
    }
]

INFRA_SERVICES = [
    {
        'name': 'Consul',
        'value': {
            'name': 'consul',
        },
    },
    {
        'name': 'PostgreSQL',
        'value': {
            'name': 'postgresql',
        },
    }
]


def mount_os_info():
    consul_client = ConsulClient(host=os.getenv('CONSUL_HOST', '127.0.0.1'))
    consul_client.connect()

    display_width = 1920
    display_height = 1080

    # get screen resolution
    try:
        display_width = get_monitors()[0].width
        display_height = get_monitors()[0].height
    except Exception as ex:
        print("Could not determine screen size, fallback is 1920x1080")
        print(ex)

    consul_client.put(key='display_width', value=display_width, prefix='shared')
    consul_client.put(key='display_height', value=display_height, prefix='shared')

if __name__ == '__main__':
    try:
        mount_os_info()
    except Exception as ex:
        print('Could not mount os information')
        print(ex)

    last_commit_sha = ''
    os.environ["BUILD_VERSION"] = ''

    if not os.path.isfile('docker-compose.local.yml'):
        users = {
            'version': '3.7',
            'networks': {
                'sites-checker': {
                    'name': 'sites-checker',
                    'driver': 'bridge'
                }
            }
        }
        with open('docker-compose.local.yml', 'w') as f:
            data = yaml.dump(users, f, sort_keys=False)

    try:
        questions = [
            {
                'type': 'list',
                'name': 'mode',
                'message': 'Choose mode',
                'choices': ['Debug'],
            },
            {
                'type': 'list',
                'name': 'service',
                'message': 'Choose service',
                'choices': [*CORE_SERVICES, Separator(), *INFRA_SERVICES],
            },
            {
                'type': 'list',
                'name': 'action',
                'message': 'Choose action',
                'choices': ['Start use cache',
                            'Start no cache (pull new image)',
                            'Stop',
                            'Restart'],
            },
        ]
        answers = prompt(questions)
        if not answers:
            exit(0)
        mode = answers['mode']
        service_folder = answers['service'].get('service_build_directory')
        working_dir = answers['service'].get('working_directory')
        service_name = answers['service'].get('name')
        scale = answers['service'].get('scale', 1)
        commands = []
        if mode == 'Prod':
            if answers['action'] == 'Start no cache (pull new image)':
                commands.append(['docker-compose',
                                 '-f', 'docker-compose.infra.yml',
                                 '-f', 'docker-compose.prod.yml',
                                 'pull', service_name])
                commands.append(['docker-compose',
                                 '-f', 'docker-compose.infra.yml',
                                 '-f', 'docker-compose.prod.yml',
                                 '-f', 'docker-compose.local.yml',
                                 'up', '-d', '--scale', f'{service_name}={scale}', service_name])

            if answers['action'] == 'Start use cache':
                commands.append(['docker-compose',
                                 '-f', 'docker-compose.infra.yml',
                                 '-f', 'docker-compose.prod.yml',
                                 '-f', 'docker-compose.local.yml',
                                 'up', '-d', '--scale', f'{service_name}={scale}', service_name])

        else:
            if service_folder and working_dir:
                git_command = subprocess.run(['git', 'log', '-1', '--pretty=format:%h', '--', f"./{service_folder}/."],
                                             stdout=subprocess.PIPE, cwd=working_dir)

                last_commit_sha = git_command.stdout.decode('utf-8')

                os.environ["BUILD_VERSION"] = last_commit_sha

            if answers['action'] == 'Start no cache (pull new image)':
                commands.append(['docker-compose',
                                 '-f', 'docker-compose.infra.yml',
                                 '-f', 'docker-compose.prod.yml',
                                 '-f', 'docker-compose.dev.yml',
                                 'build', '--no-cache', service_name])
                commands.append(['docker-compose',
                                 '-f', 'docker-compose.infra.yml',
                                 '-f', 'docker-compose.prod.yml',
                                 '-f', 'docker-compose.dev.yml',
                                 '-f', 'docker-compose.local.yml',
                                 'up', '-d', '--build', '--scale', f'{service_name}={scale}', service_name])

            if answers['action'] == 'Start use cache':
                commands.append(['docker-compose',
                                 '-f', 'docker-compose.infra.yml',
                                 '-f', 'docker-compose.prod.yml',
                                 '-f', 'docker-compose.dev.yml',
                                 '-f', 'docker-compose.local.yml',
                                 'up', '-d', '--build', '--scale', f'{service_name}={scale}', service_name])

        if answers['action'] == 'Restart':
            commands.append(['docker-compose',
                             '-f', 'docker-compose.infra.yml',
                             '-f', 'docker-compose.prod.yml',
                             'restart', service_name])

        if answers['action'] == 'Stop':
            commands.append(['docker-compose',
                             '-f', 'docker-compose.infra.yml',
                             '-f', 'docker-compose.prod.yml',
                             'stop', service_name])

        for cmd in commands:
            subprocess.run(cmd)

    except Exception as ex:
        exit(1)

    finally:
        if os.getenv('BUILD_VERSION'):
            del os.environ['BUILD_VERSION']
