# Set the current tax year here:
yr = "2022"

# Set the csv import filename here:
file_name = 'loot.csv'

proceeds = 0
cb = 0

class Order:
	def __init__(self, type, amount, total, year):
		self.type = type
		self.price = total / amount
		self.amount = amount
		self.total = total
		self.year = year
	
	def print(self):
		print(" type: " + self.type + " price: " + str(self.price) + " amount: " + str(self.amount) + " total: " + str(self.total) + " year: " + self.year)

def sell(amount, boughtOrder, sellOrder):
	return (sellOrder.price - boughtOrder.price) * amount

def proceed(amount, boughtOrder, sellOrder):
	return sellOrder.price * amount

def cost_basis(amount, boughtOrder, sellOrder):
	return boughtOrder.price * amount

def handleSell(order, cbq):
	pl = 0
	global proceeds
	global cb
	toSell = order.amount
	print('Selling order')
	order.print()
	while toSell > 0:
		boughtOrder = cbq.pop(0)
		print('To bought order')
		boughtOrder.print()
		if boughtOrder.amount >= toSell:
			if order.year == yr + '\n' or order.year == yr:
				pl += sell(toSell, boughtOrder, order)
				cb += cost_basis(toSell, boughtOrder, order)
				proceeds += proceed(toSell, boughtOrder, order)
			boughtOrder.amount -= toSell
			cbq.insert(0, boughtOrder)
			print('Partial sale of bought order, remaining:')
			boughtOrder.print()
			toSell = 0
		else:
			if order.year == yr + '\n' or order.year == yr:
				pl += sell(boughtOrder.amount, boughtOrder, order)
				cb += cost_basis(boughtOrder.amount, boughtOrder, order)
				proceeds += proceed(boughtOrder.amount, boughtOrder, order)
			toSell -= boughtOrder.amount
			toSell = round(toSell, 6)
			print('Full sale of bought order')
			print("processing ")
	print('Total pl from sale: ' + str(pl))
	return pl


f = open(file_name, 'r')
lines = f.readlines()
f.close()

orders = []

for line in lines:
	line = line.split(',')
	order = Order(line[0].lower(), float(line[1]), float(line[2]), line[3])
	orders.append(order)

cbq = [] 	# Cost-basis queue
pl = 0

# Calculate P&L from these orders
for order in orders:
	print('processing order')
	order.print()
	# If order is buy, insert into queue
	if order.type == 'buy':
		cbq.append(order)
	else:
		pl += handleSell(order, cbq)

print('')
print('Final PNL: ' + str(pl))

print('Proceeds: ' + str(proceeds))
print('Cost Basis: ' + str(cb))
print('Cost Basis Queue: ')
for order in cbq:
	order.print()