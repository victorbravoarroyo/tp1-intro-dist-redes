from flask import abort, make_response, request
import dns.resolver
from itertools import cycle

# Cache para non-custom domains para mantener un orden en RR
# Contiene pares clave:valor del tipo 'domain' (string): 'index' (iterable)
domains = {}

# Custom domains registrados
# Contiene pares clave:valor del tipo 'domain'(string): 'ip' (string)
custom_domains = {}

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

    # Resuelve dominio por primera vez
    if domain not in domains:
        try:
            result = dns.resolver.query(domain)
            ips = [ip for ip in result]
            domains[domain] = cycle(ips)
        except:
            error = {
                'error': 'domain not found'
            }
            return make_response(error, 404)

    # Obtengo siguiente IP round-robin
    result = next(domains[domain])

    item = {
        'domain': domain,
        'ip': str(result),
        'custom': False
    }

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
        error = {
            "error": "payload is invalid"
        }
        return make_response(error, 400)

    if domain in custom_domains:
        existingCustom = {
            "error": "custom domain already exists"
        }
        return make_response(existingCustom, 400)

    custom_domains[domain] = ip
    item = {
        'domain': domain,
        'ip': ip,
        'custom': True
    }

    return make_response(item, 201)

def editar(domain, **kwargs):
    """
    Esta funcion maneja el request PUT /api/domains/{domain}

    :param body: custom domain a sobre-escribir
    :return: 200 domain, 404 no existe domain, 400 mal formato
    """
    body = kwargs.get('body')
    body_domain = body.get('domain')
    ip = body.get('ip')

    if domain not in custom_domains:
        error = {
            "error": "domain not found"
        }
        return make_response(error, 404)

    if domain != body_domain or not body_domain or not ip :
        error = {
            "error": "payload is invalid"
        }
        return make_response(error, 400)

    custom_domains[domain] = ip
    item = {
        'domain': domain,
        'ip': ip,
        'custom': True
    }
    return make_response(item, 200)

def borrar(domain):
    """
    Maneja DELETE /custom-domains/{domain}

    :domain   dominio que se quiere borrar
    :return:  200 domain, 404 dominio no encontrado
    """
    if domain not in custom_domains:
        rr = {
            'error': 'domain not found'
        }
        return make_response(rr, 404)

    rr = {
        'domain':domain,
    }

    del custom_domains[domain]

    return make_response(rr, 200)

def query_custom_domains():
    """
    Búsqueda de custom domains creados mediante parámetro 'q' en URL

    :param q: string a buscar en dominios
    :return: 200 custom_domain que satisfacen query
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
