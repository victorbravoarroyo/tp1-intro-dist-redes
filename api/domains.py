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
    pass

def agregar(**kwargs):
    pass

def borrar(domain):
    pass
