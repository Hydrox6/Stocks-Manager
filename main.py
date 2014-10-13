import urllib2

codes = []
prices = {}


base = "http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/prices-search/stock-prices-search.html?nameCode={name}&page=1"
for x in codes:
    u = urllib2.urlopen(base.format(name=x)).read()
    
