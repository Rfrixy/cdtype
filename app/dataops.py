'''number of records to consider for averaging'''
entry_limit = 5
def process_history(user):
    res = {}
    res['wpm'] = 0
    res['accuracy'] = 0
    res['dwell'] = 0
    res['flight'] = 0
    res['overlap'] = 0
    res['covar'] = 0
    if 'history' in user:
        history = user['history']
    else:
        history = {}
        return res

    count = 0
    wpm = []
    accuracy = []
    dwell = []
    flight = []
    overlap = []
    covar = []
    print('lenghtt', len(history))
    for i in history[::-1]:
        data = i['data']
        if data['bot']:
            pass
        wpm.append(data['wpm'])
        accuracy.append(data['accuracy'])
        dwell.append(data['dwell'])
        flight.append(data['flight'])
        overlap.append(data['overlap'])
        covar.append(data['covar'])
        count +=1
        if count >=entry_limit:
            break
    res['wpm'] = sum(wpm)/len(wpm)
    res['accuracy'] = sum(accuracy)/len(accuracy)
    res['dwell'] = sum(dwell)/len(dwell)
    res['flight'] = sum(flight)/len(flight)
    res['overlap'] = sum(overlap)/len(overlap)
    res['covar'] = sum(covar)/len(covar)
    return res


def decryptStringWithXORFromHex( input, key):
    while (len(key) < len(input)/2):
        key += key;
    c = ""
    for i in range(0,len(input),2):
        hexValueString = input[i:i+2]
        value1 = int(hexValueString, 16);
        value2 = ord(key[i//2]);
        xorValue = value1 ^ value2;
        c += chr(xorValue);

    return (str(c))
