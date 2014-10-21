import urllib2

codes = ["ASBE","CAMB","COG","VRP","NG."]
prices = {}


base = "http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/prices-search/stock-prices-search.html?nameCode={name}&page=1"
for x in codes:
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    u = opener.open(base.format(name=x)).read()
    u = u.split('class="table_dati"')[1].split("</table>")[0].split("<tbody>")[1].split("</tbody>")[0]
    u = u.split("</td>")
    for y in range(0,len(u)):
        if y == 0:
            t = u[y].split(">")[-1].rstrip()
            if t != x:
                break
        if y == 3:
            p = float(u[y].split(">")[-1].rstrip())
            prices[x] = p
