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