from flask import abort, make_response, request
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
        error = {
            'error': 'domain not found'
        }
        return make_response(error, 404)
        # return abort(404)

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
    Esta funcion maneja el request POST /api/domains

    :param body: custom domain a crear
    :return: 201 custom domain creada, 400 domain duplicado o body mal formado
    """
    body = kwargs.get('body')
    domain = body.get('domain')
    ip = body.get('ip')
    if not domain or not ip:
        return abort(400)

    if domain in custom_domains:
        existingCustom = {
            "error": "custom domain already exists"
        }
        return make_response(existingCustom, 400)
        # return abort(400)

    custom_domains[domain] = ip
    item = {
        'domain': domain,
        'ip': ip,
        'custom': True
    }
    return make_response(item, 201)

def agregar(**kwargs):
    """
    Esta funcion maneja el request PUT /api/domains/{domain}

    :param body: custom domain a sobre-escribir
    :return: 200 domain, 404 no existe domain, 400 mal formato
    """
    body = kwargs.get('body')
    domain = body.get('domain')
    ip = body.get('ip')
    if not domain or not ip:
        error = {
        "error": "payload is invalid"
        }
        return make_response(error, 400)
        # return abort(400)

    if domain not in custom_domains:
        return abort(404)

    custom_domains[domain] = ip
    item = {
        'domain': domain,
        'ip': ip,
        'custom': True
    }
    return make_response(item, 200)

def borrar(domain):
    if domain not in custom_domains:
        rr = {
            'error': 'domain not found'
        }
        return make_response(rr,404)
    rr = {
        'domain':domain,
    }
    del custom_domains[domain]
    return make_response(rr,200)

def query_custom_domain():
    """
    Búsqueda de custom domains creados mediante parámetro 'q' en URL
    """
    query = request.args.get('q')
    items = []

    for domain in custom_domains:
        items.append({
            'domain': domain,
            'ip': custom_domains.get(domain),
            'custom': True
        })

    if query:
        items = [item for item in items if query in item.get('domain')]

    response = {
        "items": items
    }

    return make_response(response, 200)
