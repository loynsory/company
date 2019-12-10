import http.client
import urllib.parse
import json

def sedUrl(con,str):
    conn = http.client.HTTPSConnection(con)
    url = urllib.parse.quote(str, safe=':/?=&')  # 进行url编码
    conn.request("GET", url)
    res = conn.getresponse()
    return res