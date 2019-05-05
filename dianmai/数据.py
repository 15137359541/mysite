import easyquotation

quotation = easyquotation.use('daykline')
# res = quotation.market_snapshot(prefix=True)
res = quotation.real(['00001'])
# res1 = quotation.stocks(['sz399681', 'sz000001'], prefix=True)
# res2 = quotation.funda()
res=res['00001']

print(res)
# a=[]
# for i in res:
#     b=i[:6]
#     a.append(b)
# print(a)

# print(res1)
# print(res2)
