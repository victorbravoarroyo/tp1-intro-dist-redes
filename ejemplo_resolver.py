import dns.resolver

# Resolve www.yahoo.com
result = dns.resolver.query('www.yahoo.com')
print(result[0])
