from flask import abort, make_response
import dns.resolver
import dns.rdatatype

domains = {
}

def obtener_uno(domain):
    if not domain in domains:
        domains[domain] = {'index': 0, 'custom_domains': []}

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

    total_domains += domains[domain]['custom_domains']
    index = domains[domain]['index']
    a_domain = total_domains[index]
    index += 1
    domains[domain]['index'] = index if index < len(total_domains) else 0
    return a_domain

def crear(**kwargs):
    body = kwargs.get('body')
    domain = body.get('domain')
    ip = body.get('ip')
    if not domain or not ip:
        return abort(400)

    for registers in domains.values():
        for rr in registers:
            if rr['ip'] == ip:
                return abort(400)

    rr = {
        'domain': domain,
        'ip': ip,
        'custom': True
    }

    if domain not in domains:
        domains[domain] = []
    domains[domain].append(rr)
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
