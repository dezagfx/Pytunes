from config import config
import requests
import json


def getServer(method, data):
    resp = requests.get('%s/%s' % (config.server_host, method), data=data, verify=False)
    if not resp.ok:
        print("Serviço indisponível ou parâmetros inválidos (%s)." % resp.status_code)
        return None, False
    return resp.json()

def postServer(method, data):
    resp = requests.post(
    '%s/%s'% (config.server_host, method),
    data=data,
    #data={key: json.dumps(val) for key, val in data.items()},
    verify=False
    )
    if not resp.ok:
        print("Serviço indisponível ou parâmetros inválidos (%s)." % resp.status_code)
        return None, False
    # é plausível uma operação de update não devolver nada, ou seja, 
    # temos que testar se existe alguma coisa no resp.content
    return resp.json() if resp.content else None, True