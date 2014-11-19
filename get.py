# -*- coding: cp1252 -*-
import urllib2

codes = ["ASBE","CAMB","COG","VRP","NG."]
#prices = {}

signs = {"EUR":"€","GBP":"£","USD":"$"}

bases = {"conv":"http://www.xe.com/currencyconverter/convert/?Amount={amount}&From={fom}&To={to}",
         "check":"http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/prices-search/stock-prices-search.html?nameCode={name}&page=1"}

class Stock:
    #private String code
    #private String name
    #private String currency
    #private String price

    def add(self,tag,data):
        if tag == "currency" and data == "GBX":
            setattr(self,"divb100",True)
        if tag == "price" and self.divb100:
            data = str(float(data)/100)
            del self.divb100
        setattr(self,tag,data)
        

    def curconv(self,to):
        u = opener.open(bases["conv"].format(amount=self.price,fom=self.currency,to=to)).read()
        u = u.split('<tr class="uccRes">')[1].split("</tr>")[0].split("</td>")[2]
        u = u.split(">")[1].split("&")[0]
        self.currency = to
        self.price = u

    def expand():return [self.code,self.name,signs[self.currency]+self.price]

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')] #I'm not a robot, I promise *wink wink*
        

tags = ["code","name","currency","price"]

def get(code):
    u = opener.open(bases["check"].format(name=code)).read()
    u = u.split('class="table_dati"')[1].split("</table>")[0].split("<tbody>")[1].split("</tbody>")[0]
    u = u.split("</td>")
    s = Stock()
    for y in range(0,4):
        if y == 1:
            d = u[y].split(">")[-2][:-3].strip()
        else:
            d = u[y].split(">")[-1].rstrip()
        if y == 0:
            if d != code:
                break
        else:
            s.add(tags[y],d)
    
    return s
