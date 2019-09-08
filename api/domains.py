from flask import abort, make_response
import dns.resolver
import dns.rdatatype

domains = {
}

def obtener_uno(domain):
    if domain not in domains:
        try:
            result = dns.resolver.query(domain, dns.rdatatype.A)
            domains[domain] = []
        except:
            return abort(404)

        for answer in result.response.answer:
            if answer.rdtype == dns.rdatatype.A:
                for item in answer:
                    rr = {
                        'domain': domain,
                        'ip': item.to_text(),
                        'custom': False
                    }
                    domains[domain].append(rr)

    first = domains[domain].pop(0)
    domains[domain].append(first)
    return first

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
