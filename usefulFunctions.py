def threSort(input):

    thre = []

    for item in input:
        if 'threshold' not in item:
            pass
        else:
            thre.append(item['threshold'])

    thre = sorted(thre, reverse=True)

    output = []
    for item in thre:
        for item2 in input:
            if 'threshold' not in item2:
                pass
            elif item2['threshold'] == item:
                output.append(item2)
                break
    for item in input:
        if 'threshold' not in item:
            output.append(item)
    return output


def updateConfig(conf):
    if conf['useFixedPos']:
        NewConf = {'majorVersion': 3, 'minorVersion': 2, "patchVersion": 0,
                   'fixedPosition': {"x": conf['fixedPosX'], "y": conf['fixedPosY'], "z": conf['fixedPosZ']}}
    else:
        NewConf = {'majorVersion': 3, 'minorVersion': 2, "patchVersion": 0, 'fixedPosition': None}
    conf.pop('useFixedPos')
    conf.pop('fixedPosX')
    conf.pop('fixedPosY')
    conf.pop('fixedPosZ')
    conf.pop('majorVersion')
    conf.pop('minorVersion')
    conf.pop('patchVersion')

    for item in conf:
        NewConf[item] = conf[item]

    return NewConf


def RGBA2RGB(foreground, background):
    newR = int((1 - foreground[3]) * background[0] + foreground[3] * foreground[0])
    newG = int((1 - foreground[3]) * background[1] + foreground[3] * foreground[1])
    newB = int((1 - foreground[3]) * background[2] + foreground[3] * foreground[2])

    return newR, newG, newB


def getJudFromScore(judList, score):
    scores = []
    scoresDict = []

    for element in judList:
        thre = element.get('threshold')

        if thre:
            if thre <= score:
                scores.append(thre)
                scoresDict.append(element)
        else:
            if 0 <= score:
                scores.append(0)
                scoresDict.append(element)

    high_number = 0
    for x in scores:
        if x > high_number:
            high_number = x

    return scoresDict[scores.index(high_number)]
