
import os
import json
from PyInquirer import prompt
from tabulate import tabulate
from consul_client import ConsulClient

CONFIGS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'configs'))

consul_client = ConsulClient(host=os.getenv('CONSUL_HOST', '127.0.0.1'))

if __name__ == '__main__':
    try:
        print('\n')
        table = []
        all_keys = consul_client.get_all()
        if all_keys:
            for key in all_keys:
                table.append([key['Key'],json.dumps(key['Value'],
                                                    sort_keys=True, indent=4)])
            print('Current configs in http://localhost:8500')
            print('\n')
            print(tabulate(table, headers=["Key", "Value"]))
            print('\n')
    except TypeError:
        pass
    questions = [
        {
            'type': 'list',
            'name': 'file',
            'message': 'Choose config file',
            'choices': [*os.listdir(CONFIGS_DIR)],
        }
    ]
    answers = prompt(questions)
    if not answers:
        exit(0)
    with open(os.path.join(CONFIGS_DIR, answers['file']), 'r') as f:
        json_configs = json.load(f)
        for group_key, group_config in json_configs.items():
            for key, config in group_config.items():
                consul_client.put(key, config, prefix=group_key)
