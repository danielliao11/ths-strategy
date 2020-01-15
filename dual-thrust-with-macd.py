#变量初始化区域
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
tdCycle = 5
shortCycle = 12
longCycle = 26
deaCycle = 9

#取数据区域
for i in range(0, total):
    h = get("最高价", i)
    o = get("收盘价", i)
    c = get("最低价", i)
    l = get("开盘价", i)
    hevo.save("K", h, o, l, c, i)

    highList.append(h)
    lowList.append(l)
    closeList.append(c)
    openList.append(o)


#计算数据区域
for i in range(0, total):
    # 计算 macd
    shortAvg = EMA(closeList, shortCycle, i) # 短周期移动平均
    longAvg = EMA(closeList, longCycle, i) # 长周期移动平均
    diff = shortAvg - longAvg
    diffList.append(diff) # 构建 diff 列表
    dea = EMA(diffList, deaCycle, i)
    deaList.append(dea) # 构建 dea 列表
    macd = 2 * (diff - dea)
    # 通过macd判断市场方向
    # 金叉上行
    if ((diff - dea) > 0) and (diffList[i - 1] <= deaList[i -1]):
        ks = 0.5
        kx = 0.7
    # 死叉下行
    elif ((diff - dea) < 0) and (diffList[i - 1] >= deaList[i -1 ]):
        ks = 0.7
        kx = 0.5
    # 否则震荡
    else:
        ks = 0.7
        kx = 0.7
    
    # 构建dual trust 通道
    hh = HHV(highList, tdCycle, i) # 前n日最高价
    lc = LLV(closeList, tdCycle, i) # 前n日最低收盘价
    hc = HHV(closeList, tdCycle, i) # 前n日最高收盘价
    ll = LLV(lowList, tdCycle, i) # 前n日最低价
    range = max(hh - lc, hc - ll) # 确定通道范围
    buyLine = o + ks * range
    sellLine = o - kx * range
    
    save("B", buyLine, i)
    save("S", sellLine, i)

#画线区域
draw.kline("K")
draw.curve("B", 00)
draw.curve("S", 03)
