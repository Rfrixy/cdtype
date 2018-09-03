import statistics
# TODO: split function into many

def process_dwell(data):
    ku = data['ku'][:]
    kd = data['kd'][:]
    dwell_times = []
    dwell_list= []
    ku = [ x for x in ku if x[1]!=None]
    kd = [ x for x in kd if x[1]!=None]
    while ku:
        el = ku.pop(0)
        i = 0
        while i < len(kd) and el[1] > kd[i][1]:
            if el[0].lower() == kd[i][0].lower():
                dwell_list.append([ el[0].lower() , kd[i][1],  el[1] ])
                dwell_times.append(el[1] - kd[i][1])
                kd.pop(i)
                i-=1
            i+=1
    return dwell_list,dwell_times

def process_accuracy(data,text):
    kd = data['kd'][:]
    kd = [ x for x in kd if x[1]!=None]
    text = text.lower()
    index = 0
    errors = 0
    for i in kd:
        if i[0].lower() == text[index]:
            index +=1
        else:
            errors +=1
    return errors

def process_overlap(dwell_list):
    overlap_list = []
    for i in range(len(dwell_list)-1):
        if dwell_list[i][2] > dwell_list[i+1][1]:
            overlap_list.append([dwell_list[i][0],dwell_list[i+1][0], dwell_list[i][2] - dwell_list[i+1][1]])
    return overlap_list


def process_wpm_brackets(timing,text):
    wpm_brackets = []
    wpm_list = []
    n = len(text)//8
    i = 0
    while i < len(text)-1:
        f = i+n
        if f + n >= len(text):
            f = len(text)-1
        curr_wpm =   (f-i)*12/ ((timing[f] - timing[i])/1000)
        wpm_brackets.append([curr_wpm,text[i:f]])
        wpm_list.append(curr_wpm)
        i = f

    denom = 0
    for w in wpm_list:
        denom += 1/w
    recalculated_wpm = len(wpm_list)/denom

    return wpm_brackets,recalculated_wpm

def process_list(data,text):
    ts_list = data['all_keys']
    text = text['text']

    if not text:
        return (False,)
    if len(ts_list) != len(text):
        return (False,)

    timing = ts_list[:]
    wpm =  (len(timing)* 12)/ (timing[-1]/1000)
    wpm = round(wpm)
    errors = process_accuracy(data,text)
    dwell_list,dwell_times = process_dwell(data)
    # print(dwell_list,'dwell list')
    overlap_list = process_overlap(dwell_list)
    overlap_percent = len(overlap_list)/len(dwell_list)
    # print(overlap_list,'overlap list')
    flight = data['flight']
    flight_list = []
    for f in flight:
        flight_list.append(f[1])
    # print(flight_list)
    # print('mflight stddev',statistics.stdev(flight_list))
    devn = statistics.stdev(flight_list)
    mean = statistics.mean(flight_list)
    covar = devn/mean
    wpm_brackets,recalculated_wpm = process_wpm_brackets(timing,text)
    if recalculated_wpm - wpm > 5 or recalculated_wpm - wpm < -5:
        return(False,)

    data = {}
    data['wpm'] = wpm
    data['accuracy'] = len(text)/(len(text) + errors)
    data['dwell'] = statistics.mean(dwell_times)
    data['flight'] = statistics.mean(flight_list)
    data['flightstd'] = statistics.stdev(flight_list)
    data['dwellstd'] = statistics.stdev(dwell_times)
    data['overlap'] = overlap_percent
    data['covar'] = covar
    data['text'] = text
    # data['brackets'] = wpm_brackets
    print(data)

    return ( True, wpm, data ,wpm_brackets)

# imp params decreasing: overlap,  dwell stddev, dwell, flight,correct covar,
    return (False,)
