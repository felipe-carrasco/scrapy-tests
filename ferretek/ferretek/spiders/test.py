import re
url = 'Kit Taladro Percutor ENERGY ID13/2/220/K 13mm'

print(f"Original:\t{url}")
print(f"Título:\t\t{url.title()}")

price = ' $58.990'

print(re.sub(' |\$|\.', '', price))

sku = 'SKU: 123987'

print(sku.replace('SKU: ', ''))
