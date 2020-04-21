import re
url = 'Kit Taladro Percutor ENERGY ID13/2/220/K 13mm'

print(f"Original:\t{url}")
print(f"Título:\t\t{url.title()}")

price = ' $58.990'

print(re.sub(' |\$|\.', '', price))

sku = 'SKU: 123987'

print(sku.replace('SKU: ', ''))

hola = '1 2 3 4 5'.split()
hola = '1 2 3 4 5'


symbols = '"#$%&/'
codes = [ord(symbol) for symbol in symbols]
print(codes)

colors = ['black', 'white', 'red']
sizes = ['S', 'M', 'L']
tshirts = [(color, size) for color in colors for size in sizes]
print(tshirts)
