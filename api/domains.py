from flask import abort, make_response
import dns.resolver
import dns.rdatatype

custom_domains = {
}

def obtener_uno(domain):
    if not domain in custom_domains:
        custom_domains[domain] = {'index': 0, 'items': []}

    try:
        result = dns.resolver.query(domain)
    except:
        return abort(404)

    total_domains = []
    for answer in result.response.answer:
        if answer.rdtype == dns.rdatatype.A:
            for item in answer:
                rr = {
                    'domain': domain,
                    'ip': item.to_text(),
                    'custom': False
                }
                total_domains.append(rr)

    total_domains += custom_domains[domain]['items']
    index = custom_domains[domain]['index']
    a_domain = total_domains[index]
    index += 1
    custom_domains[domain]['index'] = index if index < len(total_domains) else 0
    return a_domain

def crear(**kwargs):
    body = kwargs.get('body')
    domain = body.get('domain')
    ip = body.get('ip')
    if not domain or not ip:
        return abort(400)

    for entries in custom_domains.values():
        for item in entries['items']:
            if item['ip'] == ip:
                return abort(400)

    rr = {
        'domain': domain,
        'ip': ip,
        'custom': True
    }

    if not domain in custom_domains:
        custom_domains[domain] = {'index': 0, 'items': []}

    custom_domains[domain]['items'].append(rr)
    return make_response(rr, 201)

def agregar(**kwargs):
    body = kwargs.get('body')
    domain = body.get('domain')
    ip = body.get('ip')
    if not domain or not ip:
        return abort(400)

    if not domain in domains:
        return abort(404)

    rr = {
        'domain': domain,
        'ip': ip,
        'custom': True
    }

    domains[domain].append(rr)
    return make_response(rr, 200)
