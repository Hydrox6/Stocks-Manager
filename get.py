# -*- coding: cp1252 -*-
import urllib2

codes = ["ASBE","CAMB","COG","VRP","NG."]
#prices = {}

#signs = {"EUR":[u"€",True],"GBP":[u"£",True],"USD":[u"$",True]}

bases = {"conv":"http://www.xe.com/currencyconverter/convert/?Amount={amount}&From={fom}&To={to}",
         "check":"http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/prices-search/stock-prices-search.html?nameCode={name}&page=1"}

class Stock:
    #private String Code
    #private String Name
    #private String Currency
    #private String Price
    #private String ocurrency
    #private String oprice
    #private temp boolean divb100

    def __init__(self,preload=None):
        if not preload == None:
            self.__dict__.update(preload)

    def add(self,tag,data):
        if tag == "Currency" and data == "GBX":
            setattr(self,"divb100",True)
            setattr(self,"ocurrency",data)
            setattr(self,"Currency","GBP")
        elif tag == "Price" and self.divb100:
            setattr(self,"oprice",data)
            data = str(float(data)/100)
            del self.divb100
            setattr(self,tag,data)
        else:
            setattr(self,tag,data)


    def curconv(self,to):
        old = self.Price
        ocur = self.Currency
        oto = to
        ncur = to
        if self.Currency == "GBX":
            old = float(old)/100
            ocur = "GBP"
        elif to == "GBX":
            ncur = "GBP"
        u = opener.open(bases["conv"].format(amount=self.Price,fom=self.Currency,to=to)).read()
        u = u.split('<tr class="uccRes">')[1].split("</tr>")[0].split("</td>")[2]
        u = "{0:.2f}".format(float(u.split(">")[1].split("&")[0]))
        if oto == "GBX":
            to = "GBX"
            u = str(float(u)*100)
        self.currency = to
        self.price = u
        self.Currency = to
        self.Price = u

    def expand(self):return [self.Code,self.Name,self.Currency+" "+self.Price]

    def dictify(self):return {key:value for key, value in self.__dict__.items() if not key.startswith('__') and not callable(key)}

"""
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
        print before.split(",")
        raw_input()
"""

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')] #I'm not a robot, I promise *wink wink*
        
#getSigns()

tags = ["Code","Name","Currency","Price"]

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
    s.add("Code",code)
    return s
