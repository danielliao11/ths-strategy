# 变量初始化区域
highList = []
lowList = []
closeList = []
openList = []
hhList = []
lcList = []
hcList = []
llList = []
diffList = []
deaList = []
trList = []
tdPeriod = 3
shortPeriod = 12
longPeriod = 26
deaPeriod = 9
trPeriod = 15

# 取数据区域
for i in range(0, total):
    h = get("最高价", i)
    o = get("开盘价", i)
    c = get("收盘价", i)
    l = get("最低价", i)
    hevo.save("K", h, o, l, c, i)

    highList.append(h)
    lowList.append(l)
    closeList.append(c)
    openList.append(o)


# 计算数据区域
for i in range(0, total):
    # 计算 macd
    shortAvg = EMA(closeList, shortPeriod, i - 1) # 短周期移动平均
    longAvg = EMA(closeList, longPeriod, i - 1) # 长周期移动平均
    diff = shortAvg - longAvg
    diffList.append(diff) # 构建 diff 列表
    dea = EMA(diffList, deaPeriod, i)
    deaList.append(dea) # 构建 dea 列表
    macd = 2 * (diff - dea)
    # 通过macd判断市场方向
    # 金叉上行
    if ((diff - dea) > 0) and (diffList[i - 1] <= deaList[i -1]):
        ks = 0.3
    # 死叉下行
    elif ((diff - dea) < 0) and (diffList[i - 1] >= deaList[i - 1]):
        ks = 0.5
    # 否则震荡
    else:
        ks = 0.5
    
    # 构建dual trust 通道
    hh = HHV(highList, tdPeriod, i - 1) # 前n日最高价
    lc = LLV(closeList, tdPeriod, i - 1) # 前n日最低收盘价
    hc = HHV(closeList, tdPeriod, i - 1) # 前n日最高收盘价
    ll = LLV(lowList, tdPeriod, i - 1) # 前n日最低价
    range = max(hh - lc, hc - ll) # 确定通道范围
    # 构建 TR
    h = highList[i - 1]
    l = lowList[i - 1]
    lastClose = closeList[i - 1]
    tr = max(max(h - l, abs(lastClose - h)), abs(lastClose - l))
    trList.append(tr)
    atrL = MA(trList, longPeriod, i - 1)
    atrS = MA(trList, trPeriod, i - 1)
    hightest = HHV(highList, trPeriod, i - 1)
    currentOpen = openList[i]
    buyLine = currentOpen + ks * range
    sellLine = max(abs(hightest - 3*atrS), abs(hightest - 3*atrL), abs(lastClose - 1.5*atrS), abs(lastClose - 1.5*atrL))
    
    save("B", buyLine, i)
    save("S", sellLine, i)

#画线区域
draw.kline("K")
draw.curve("B", 0)
draw.curve("S", 7)