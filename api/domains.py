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
            abort(404)

        for answer in result.response.answer:
            if answer.rdtype == dns.rdatatype.A:
                for item in answer:
                    info_domain = {
                        'domain': domain,
                        'ip': item.to_text(),
                        'custom': False
                    }
                    domains[domain].append(info_domain)

    first = domains[domain].pop(0)
    domains[domain].append(first)
    return first
