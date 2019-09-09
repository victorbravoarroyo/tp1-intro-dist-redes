from flask import abort, make_response
import dns.resolver
import dns.rdatatype

# Custom domains registrados
# Contiene pares clave:valor del tipo 'domain'(string): 'ip' (string)
custom_domains = {}

# Indices para los non-custom domains para mantener un orden en RR
# Contiene pares clave:valor del tipo 'domain' (string): 'index' (int)
indexes = {}

def obtener_uno(domain):
    """
    Esta funcion maneja el request GET /api/domains/{domain}

    :domain: domain del cual se quiere obtener su IP
    :return: 200 domain, 404 domain no encontrado
    """
    if domain in custom_domains:
        item = {
            'domain': domain,
            'ip': custom_domains.get(domain),
            'custom': True
        }
        return make_response(item, 200)

    try:
        result = dns.resolver.query(domain)
    except:
        return abort(404)

    if domain not in indexes:
        indexes[domain] = 0

    index = indexes.get(domain) % len(result)
    item = {
        'domain': domain,
        'ip': str(result[index]),
        'custom': False
    }
    indexes[domain] = index + 1
    return make_response(item, 200)


def crear(**kwargs):
    """
    Esta funcion maneja el request POST /api/domain

    :param body: custom domain a crear
    :return: 201 custom domain creada, 400 domain duplicado o body mal formado
    """
    body = kwargs.get('body')
    domain = body.get('domain')
    ip = body.get('ip')
    if not domain or not ip:
        return abort(400)

    if domain in custom_domains:
        return abort(400)

    custom_domains[domain] = ip
    item = {
        'domain': domain,
        'ip': ip,
        'custom': True
    }
    return make_response(item, 201)

def agregar(**kwargs):
    pass

def borrar(domain):
    pass
