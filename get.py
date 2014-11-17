# -*- coding: cp1252 -*-
import urllib2

codes = ["ASBE","CAMB","COG","VRP","NG."]
#prices = {}

currencies = {"EUR":"EUR","GBX":"GBP"}
signs = {"EUR","€","GBP":"£","USD":"$"}

bases = {"conv":"http://www.xe.com/currencyconverter/convert/?Amount={amount}&From={fom}&To={to}",
         "check":"http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/prices-search/stock-prices-search.html?nameCode={name}&page=1"}

class Stock:
    #private String code
    #private String name
    #private String currency
    #private String price

    def add(self,tag,data):setattr(self,tag,data)

    def curconv(self,to):
        u = opener.open(bases["conv"].format(amount=self.price,fom=currencies[self.currency],to=to)).read()
        u = u.split('<tr class="uccRes">')[1].split("</tr>")[0].split("</td>")[2]
        u = u.split(">")[1].split("&")[0]
        self.currency = to
        self.price = u

    def expand():return [self.code,self.name,signs[self.currency]+self.price]

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]  
        

tags = ["code","name","currency","price"]

def get(code):
    #for x in codes:
    u = opener.open(bases["check"].format(name=x)).read()
    u = u.split('class="table_dati"')[1].split("</table>")[0].split("<tbody>")[1].split("</tbody>")[0]
    u = u.split("</td>")
    s = Stock()
    for y in range(0,4):
        if y == 1:
            d = u[y].split(">")[-2][:-3].strip()
        else:
            d = u[y].split(">")[-1].rstrip()
        if y == 0:
            if d != x:
                break
        else:
            s.add(tags[y],d)
    
    return s


sss["CAMB"].curconv("EUR")
