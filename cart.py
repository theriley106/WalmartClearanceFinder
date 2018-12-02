import requests
import json

headers = {
    'origin': 'https://www.walmart.com',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,es-US;q=0.8,es;q=0.6,ru-BY;q=0.4,ru;q=0.2,en;q=0.2',
    'omitcorrelationid': 'true',
    'omitcsrfjwt': 'true',
    'cookie': 'TBV=7; __distillery=5644c81_f14700b2-4bf7-4580-b67a-949c4afd20b2-1d2834bf0-650ad2a2b42f-bcd1; WMR=p1-1|p2-1|p3-1|p4-0; cid_csid=43a67794-6501-4634-b96c-7dc334ee21b9; akavpau_p4=1543778394~id=a507aebb53c4e5e504de0e1948423286; search.perf.metric=timerPromiseAll=831ms|timerSearchAction=831ms|timerHeaderAction=21ms|timerFooterAction=10ms|timerPreso=831ms; location-data=29678%3ASeneca%3ASC%3A%3A8%3A1|v7%2C3fh%2C2hi%2Cb0%2Chw%2C3ff%2Cuv%2C2gn%2Cv6%2Chj||3|1|; DL=29678%2C%2C%2Cip%2C29678%2C%2C; t-loc-zip=1543777825980|29678; akavpau_p6=1543778426~id=f208bcd0427c981643bfd3bc2be01a12; akavpau_p3=1543778431~id=850c5727329e83d371d867487b807247; athrvi=RVI~h23b5d9f1-h21646911-h3a55f22c-h30f5f9d-h30b61e3-h26462720-h18f7ae16-h228883ab-h239842e-h15524716; ACID=33fa9478-fcb8-45f9-8797-0440575c7c59; hasACID=1; auth=MTAyOTYyMDE4z2fyiF2zMv1%2BHKMZMWtjMKyXAgiPhPwN0A6ucSf%2BhFVOLvCS04rWDl16cCoNUQ4scOH1aZ9fJVAFE%2FOllCxHisc4N6nNKhLQjmIkx1LJyqkBl%2FqhhD3osBYyyGILT4QC767wuZloTfhm7Wk2KcjygsAEeU%2BeKCMhfP9XV060SY9dkSqPY1AlP3Fh2tR21I7ABDl2fWq1GTRcxg9nhe9XpC1fAucvwxlIASc7ltVfS5BGyEMqGry%2B0lIRqFvmUM8k6c%2BAgxjITzu6vjMSG%2FGMWt2TdfwrBECE7F8OvP0yzZ%2FeNmqM%2FMZ57C52kc8%2FfxGD%2BVh3A66PnPyTQNLSkVTv5sdc42qG34K54SL%2BMUxeikweNysoawgE0%2F7YK557VeAaFD%2BYMz0QJ7tBZV5hWqIKTQ%3D%3D; type=GUEST; cart-item-count=1; AID=wmlspartner%3Dlw9MynSeamY%3Areflectorid%3D06236665012842608445%3Alastupd%3D1543777840508; com.wm.reflector="reflectorid:06236665012842608445@lastupd:1543777840509@firstcreate:1542822649217"; CRT=4c14805e-25e2-4cb7-a561-496872530d5f; hasCRT=1; TS01a3099b=0130aff232e37eb02b2ca0c5af1694f7fc13443508bd273756f149f54833f106abc4487eb936138b339ec29d5202d54789d16f9294; akavpau_p0=1543778442~id=4dc16d15e49868dfe39895af398d7b8c; vtc=VBGSbr2VHQ0fcBfpK6MN_M; bstc=W0nOFeQJ0kGc21Zv781dlI; xpa=; xpm=3%2B1543777788%2BVBGSbr2VHQ0fcBfpK6MN_M~%2B0; TS011baee6=01c5a4e2f937b4c2b4c71a810b348a066ce82d1f9e0c5860b047776675c8ac6405ba3459f5b4640242e0b631a93a86c6530316dda4; TS01e3f36f=01c5a4e2f937b4c2b4c71a810b348a066ce82d1f9e0c5860b047776675c8ac6405ba3459f5b4640242e0b631a93a86c6530316dda4; TS018dc926=01c5a4e2f937b4c2b4c71a810b348a066ce82d1f9e0c5860b047776675c8ac6405ba3459f5b4640242e0b631a93a86c6530316dda4; akavpau_p2=1543778447~id=706c5cac3b94adda9d30c9162d7fdd34',
    'pragma': 'no-cache',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Mobile Safari/537.36',
    'credentials': 'include',
    'content-type': 'application/json',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'cache-control': 'no-cache',
    'authority': 'www.walmart.com',
    'referer': 'https://www.walmart.com/cart?source=pac',
}

data = '{"quantity":"3"}'

response = requests.put('https://www.walmart.com/api/v3/cart/:CRT/items/33e2e4e1-fd3f-46f7-99c1-3c9950cde2a0', headers=headers, data=data)
print json.dumps(response.json())
