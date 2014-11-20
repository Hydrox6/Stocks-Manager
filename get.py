# -*- coding: cp1252 -*-
import urllib2

codes = ["ASBE","CAMB","COG","VRP","NG."]
#prices = {}

signs = {"EUR":[u"€",True],"GBP":[u"£",True],"USD":[u"$",True]}

bases = {"conv":"http://www.xe.com/currencyconverter/convert/?Amount={amount}&From={fom}&To={to}",
         "check":"http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/prices-search/stock-prices-search.html?nameCode={name}&page=1"}

class Stock:
    #private String code
    #private String name
    #private String currency
    #private String price
    #private String ocurrency
    #private String oprice
    #private temp boolean divb100

    def add(self,tag,data):
        if tag == "currency" and data == "GBX":
            setattr(self,"divb100",True)
            setattr(self,"ocurrency",data)
        if tag == "price" and self.divb100:
            setattr(self,"oprice",data)
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


def getSigns():
    u = opener.open("http://www.xe.com/iso4217.php").read()
    u = u.split('class="sPg_tbl tablesorter"')[1].split("</table>")[0].split("<tbody>")[1].split("</tr>")
    for x in u:
        u2 = x.split('href="')[1].split('"')[0]
        v = opener.open("http://www.xe.com"+u2).read()
        sign = v.split('class="currencystats"')[1].split('<div class="currencyprofile">')[0].split("</p>")[1].split("</strong>")[1].split("<strong>")[0].decode("utf-8").strip()
        before = v.split('class="currencyprofile"')[1].split('</div>')[1].split("Banknotes:")[1].split("Rarely Used:")[0].decode("utf-8")#.split(",")#)
        print sign
        print before
        print before.split(",")[1]
        raw_input()
        


opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')] #I'm not a robot, I promise *wink wink*
        
getSigns()

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
