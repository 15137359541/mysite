# mysite
简单的点买界面，进行止损止盈


如同同花顺类似，股票价格实时更新，股票的价格及其走势可以展示出来，但当某个股票价格达到自己设置的止损点或者止盈点
股票自动买卖，达到自动止损止盈的效果  


通过保存在数据库mongo中的数据，进行选股的操作，通过某些方式，选择最优的股票；前端使用highchart进行数据分许，图表的绘制，

前后端数据的传递使用ajax，get方式，设置界面中价格的更新是实时的，每半秒更新一次，后端使用了django框架，涉及响应页面，重定向，

tushare第三方库，新浪实时数据，券商的登陆，以及账号的资金状况，交易记录处理