from flask import abort, make_response
import dns.resolver
import dns.rdatatype

custom_domains = {
}

def obtener_uno(domain): 
    
    if domain not in custom_domains:
        try:
            result = dns.resolver.query(domain)
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
            
            custom_domains[domain] = {'index': 0, 'items': total_domains}
        except:
            return abort(404)

    index = custom_domains[domain]['index']
    len_array_domains = len(custom_domains[domain]['items'])
    a_domain = custom_domains[domain]['items'][index]
    custom_domains[domain]['index'] = (index + 1) % len_array_domains
    return make_response(a_domain,200)

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

    if not domain in custom_domains:
        return abort(404)

    rr = {
        'domain': domain,
        'ip': ip,
        'custom': True
    }

    custom_domains[domain]['items'].append(rr)
    return make_response(rr, 200)

def borrar(domain):
    if domain not in custom_domains:
        return abort(404)
    rr = {
        'domain':domain,
    }
    del custom_domains[domain]
    return make_response(rr,200)