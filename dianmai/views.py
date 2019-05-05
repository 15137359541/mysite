import easyquotation,json
import easytrader,time,requests
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from dianmai.models import *
import numpy as np
import talib
import tushare as ts
import re

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def pic(request):
    if request.method =="GET":
        Datas = MysqlData()
        if request.session.get('money'):
            money=request.session.get('money')
        else:
            money=''
        print("sess中request.session.get('zhiying')",request.session.get('zhiying'))
        if request.session.get('gupiao'):
            gupiao=request.session.get('gupiao')
        else:
            gupiao=''
        if request.session.get('zhiying'):
            zhiying=request.session.get('zhiying')
        else:
            zhiying=''
        if request.session.get('zhisun'):
            zhisun=request.session.get('zhisun')
        else:
            zhisun=''
        if request.session.get('juanshang'):
            juanshang=request.session.get('juanshang')
        else:
            juanshang=''
        context = {
            'Datas':Datas,
            "money":money,
            'zhiying': zhiying,
            'zhisun': zhisun,
            'gupiao': gupiao,
            'juanshang':juanshang
        }
        return  render(request,'dianmai/3.html',context)
    else:
        name = request.POST['name']
        print('所选择的股票是', name)

        list_data=getData(name)
        price,open=getPrice(name)
        res={
            'list_data':list_data,
            'pri':price,
            'code':name,
            'open':open
             }

        return HttpResponse(json.dumps(res), content_type='application/json')

#获取个证券公司的数据demo01
# def getData(name):
#     quotation = easyquotation.use('daykline')
#     res = quotation.real([name])
#     res = res[name]
#
#     day_data = []
#     for i in res:
#         b = i[:6]
#         day_data.append(b)
#     return day_data

#获取个证券公司的数据demo02
# def getData(name):
#     '''
#     url=http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=[市场][股票代码]&scale=[周期]&ma=no&datalen=[长度]
#     返回结果：获取5、10、30、60
#     分钟JSON数据；day日期、open开盘价、high最高价、low最低价、close收盘价、volume成交量；向前复权的数据。
#
#     注意，最多只能获取最近的1023个数据节点。
#     :param name:
#     :return:
#     '''
#
#     url = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=' + name + '&scale=60&ma=no&datalen=1024'
#     # print(url)
#     res = requests.get(url)
#     res = res.text
#     res = res[1:-1].replace('day', "'day'").replace('open', '"open"').replace('high', '"high"').replace('low',
#                                                                                                         '"low"').replace(
#         'close', '"close"').replace('volume', '"volume"')
#     # print(res)
#     list1 = eval(res)
#     # print(list1)
#
#     day_data = []
#     for item in list1:
#         eachData = []
#         for itemi, value in item.items():
#             if itemi == "close":
#                 eachData.insert(2, value)
#             else:
#                 eachData.append(value)
#         day_data.append(eachData)
#     return day_data


#-------获取个证券公司的数据demo03--------
# 创建MACD买卖信号，包括三个参数fast period, slow period, and the signal
# 注意：MACD使用的price必须是narray
def dealMACD(prices, fastperiod=12, slowperiod=26, signalperiod=9):
    '''
    参数设置:
        fastperiod = 12
        slowperiod = 26
        signalperiod = 9

    返回: macd - signal
    '''
    dif_l, dea_l, macd_l = talib.MACD(prices,
                                    fastperiod=fastperiod,
                                    slowperiod=slowperiod,
                                    signalperiod=signalperiod)
    dif_l=transformNan(dif_l)
    dea_l=transformNan(dea_l)
    macd_l=transformNan(macd_l)

    return dif_l,dea_l,macd_l*2

#将返回结果中的nan都转为0
def transformNan(reg):
    for i in range(len(reg)):
        # print(reg[i])
        # print(type(reg[i]))
        if np.isnan(reg[i]):
            # print("转换")
            reg[i]=0
            # print(reg[i])
    return reg

def getData(name):
    name = re.search('(\d+)', name).group(1)
    res = ts.get_h_data(name, start='2017-06-16',end='2018-07-18')
    # print(res)
    #获取DataFrame的序列，索引

    res_date = res.index.tolist()
    res_date.reverse()
    res_date_fin=[]
    for each_date in res_date:
        otherStyleTime = each_date.strftime("%Y-%m-%d")
        res_date_fin.append(otherStyleTime)


    res_open = res['open'].values.tolist()
    res_open.reverse()
    res_close = res['close'].values.tolist()
    res_close.reverse()
    res_close = np.array(res_close)

    res_high = res['high'].values.tolist()
    res_high.reverse()
    res_low = res['low'].values.tolist()
    res_low.reverse()
    res_volume = res['volume'].values.tolist()
    res_volume.reverse()

    res_dif, res_dea, res_macd = dealMACD(res_close)

    res_tag = []
    for i in range(len(res_open)):
        res_tag.append(1)
    fin_res=zip(res_date_fin,res_open,res_close,res_low,res_high,res_volume,res_tag,res_macd,res_dif,res_dea)
    return list(fin_res)
#-----end获取个证券公司的数据demo02------



#获取股票当前价格demo01
# def getPrice(name):
#     quotation = easyquotation.use('hkquote')
#     res = quotation.real([name])
#     res = res.get(name)["price"]
#     return res
#获取股票当前价格demo02
def getPrice(name):
    '''
    JSON实时数据，以逗号隔开相关数据，数据依次是“股票名称、今日开盘价、昨日收盘价、当前价格、今日最高价、今日最低价、竞买价、竞卖价、成交股数、成交金额、买1手、买1报价、买2手、买2报价、…、买5报价、…、卖5报价、日期、时间”

    :param name:
    :return:
    '''

    url ='http://hq.sinajs.cn/list='+name
    # print(url)
    res = requests.get(url)
    res = res.text
    print(res)
    con = res.split(",")
    return con[3],con[1]
# 获取股票当前价格，并且实时刷新
def getPriceNow(request):
    try:
        if request.method =="GET":
            name = request.GET['name']
            price, open = getPrice(name)
            res = {
                'pri': price,
                'open': open
            }
            return HttpResponse(json.dumps(res), content_type='application/json')
    except:
        print("没有选择股票，没法得到价格")

#处理股票
@csrf_exempt
def dealStock(request):
    if request.method=="POST":
        context={}
        print("post传递")
        res = request.POST
        print(res)
        juanshang = request.POST['juanshang']
        gupiao = request.POST['gupiao']
        money = request.POST['money']
        time = request.POST['time']
        zhiying = request.POST['zhiying']
        zhisun = request.POST['zhisun']

        try:
            ischeck = request.POST['allow']
            print('券商：',juanshang)
            print('股票:', gupiao)
            print("money:", money)
            print("time", time)
            print('zhiying:', zhiying)
            print('zhisun:', zhisun)
            #不能投机取巧，不能这样写
            # request.session={
            #     'zhiying': zhiying,
            #     "money":money,
            #     'zhisun':zhisun,
            #     'gupiao':gupiao,
            #
            # }
            request.session['money'] = money
            request.session['zhiying'] = zhiying
            request.session['zhisun'] = zhisun
            request.session['gupiao'] = gupiao
            request.session['juanshang'] = juanshang
            # return render(request, 'dianmai/3.html')
            return HttpResponseRedirect('/dianmai/')
        except:
            context['error_tip2'] = 'x'
            return HttpResponseRedirect('/dianmai/')

#华泰登陆：
def htLogin():
    # 登录 easytrader 支持的用户
    user = easytrader.use('ht_client')
    # print("user是：", user)
    user.prepare(user='666629279969', password='062929', comm_password="062929AAA")
    return user
#国金登陆
def gjLogin():
    user = easytrader.use('gj_client')
    user.prepare(user='35222745', password='062929')
    return user

#华泰证券处理
def ht():
    user = htLogin()
    # 获取持仓
    print("持仓", user.position)
    time.sleep(1)

    # 资金状况
    print('资金状况；', user.balance)
    time.sleep(1)

    # 当日成交
    print('当日成交：', user.today_trades)
    time.sleep(1)

    # 当日委托
    print("当日委托", user.today_entrusts)
    time.sleep(1)

#华泰可用价格
def htPrice():
    user = htLogin()
    # 资金状况
    # print('资金状况；', user.balance)
    price = user.balance.get("可用金额")
    # print(price)
    return price
#国金可用价格
def gjPrice():
    user = gjLogin()
    print(user.balance)
    price = user.balance.get("可用金额")
    return float(price)
#证券分类
def securities(request):
    if request.method =="GET":
        sec = request.GET['sec']
        if sec =="华泰证券":
            price = htPrice()

        elif sec =="国金证券":
            price=gjPrice()

        elif sec =="银河证券":
            price=10000

        elif sec =="同花顺":
            price=200000

        elif sec =="雪球":
            price="雪球"

        else:
            price='None'

        res = {
            'price': price
        }

        return HttpResponse(json.dumps(res), content_type='application/json')


#从数据库中获取所有的数据demo01
# def MysqlData():
#     datas = Security.objects.all()
#     return datas

#从数据库中获取所有的数据demo02
def MysqlData():
    #直接调用easyquotation这个函数
    quotation = easyquotation.use('sina')
    res = quotation.market_snapshot(prefix=True)
    secrities_data = {}
    for item, value in res.items():
        secrities_data[item] = value['name']
    return secrities_data

