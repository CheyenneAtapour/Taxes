# This program calculates P&L from Binance generated CSV trade history using FIFO accounting

from argparse import ArgumentParser

class Order:
	def __init__(self, date, market, type, price, amount, total, fee, feecoin):
		self.date = date
		self.market = market
		self.type = type
		self.price = price
		self.amount = amount
		self.total = total
		self.fee = fee
		self.feecoin = feecoin

	def print(self):
		print("date: " + self.date + " market: " + self.market + " type: " + self.type + " price: " + self.price + " amount: " + self.amount)

def sell(amount, boughtOrder, sellOrder):
	return (sellOrder.price - boughtOrder.price) * amount

def handleSell(order, cbq):
	pl = 0
	toSell = order.amount
	while toSell > 0:
		boughtOrder = cbq.pop(0)
		if boughtOrder.amount >= toSell:
			pl += sell(toSell, boughtOrder, order)
			boughtOrder.amount -= toSell
			cbq.insert(0, boughtOrder)
			toSell = 0
		else:
			pl += sell(boughtOrder.amount, boughtOrder, order)
			toSell -= boughtOrder.amount
	return pl

# Set up command line file parser
parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="myFile", help="Open specified file")
args = parser.parse_args()
myFile = args.myFile

# Open up the csv file for reading
f = open(myFile)
lines = f.readlines()
f.close()

orders = []

# Skip the first header line, gather relevant data
lines = lines[1:]
for line in lines:
	line = line.split(',')
	order = Order(line[0], line[1], line[2], float(line[3]), float(line[4]), line[5], line[6], line[7])
	orders.append(order)

# Put the orders in chronological order
orders.reverse()

cbq = [] 	# Cost-basis queue
pl = 0

# Calculate P&L from these orders
for order in orders:
	# If order is buy, insert into queue
	if order.type == 'BUY':
		cbq.append(order)
	else:
		pl += handleSell(order, cbq)
print(pl)