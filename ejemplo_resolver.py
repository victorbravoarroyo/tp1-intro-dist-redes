import dns.resolver

# Resolve www.yahoo.com
result = dns.resolver.query('www.yahoo.com')
for answer in result.response.answer:
    print(answer)
