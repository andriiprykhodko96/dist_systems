import consul
import json
import uuid
from random import choice
consul_client = consul.Consul(host='127.0.0.1', port=8500)


def register_ms(ms, ms_port):
    ms_id = str(uuid.uuid4())
    consul_client.agent.service.register(
        ms,
        ms_id,
        address='localhost',
        port = ms_port
    )
    return ms_id


def deregister_ms(ms):
    consul_client.agent.service.deregister(ms)


def get_service_address_port(ms):
    services_tmp = [
        f"http://{service_info['Address']}:{service_info['Port']}"
        for _, service_info in consul_client.agent.services().items()
        if service_info['Service'] == ms
    ]
    return choice(services_tmp) if services_tmp else None


def store_kv(key, value):
    consul_client.kv.put(key, value)


def get_kv(key):
    _, config = consul_client.kv.get(key)
    return config['Value'] if config else None

hz_configs = {
    "cluster_name": "dev",
    "cluster_members": [
        "127.0.0.1:5701",
        "127.0.0.1:5702",
        "127.0.0.1:5703"
    ],
    "map_name": "log_map",
}

mq_configs = {
    "queue_name": "mq"
}

hz_configs_json = json.dumps(hz_configs)
store_kv('hz_configs', hz_configs_json)

mq_configs_json = json.dumps(mq_configs)
store_kv('mq_configs', mq_configs_json)