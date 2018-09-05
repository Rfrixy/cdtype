import statistics
import uuid

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

def process_flight(data):
    flight = data['flight']
    flight_list = []
    flight_dict = {}

    for f in flight:
        flight_list.append(f[1])
        if f[0] in flight_dict:
            flight_dict[f[0]].append(f[1])
        else:
            flight_dict[f[0]] = [f[1]]

    flight_result = []
    for k in flight_dict:
        if len(flight_dict[k])>4:
            flight_result.append([k, sum(flight_dict[k])/len(flight_dict[k])])
        flight_dict[k] = sum(flight_dict[k])/len(flight_dict[k])

    l = sorted(flight_result,key = lambda x: x[1], reverse = True)

    return flight_list,l

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
    result = {}
    extra_data = {}
    verbose_data = {}
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
    overlap_list = process_overlap(dwell_list)
    overlap_percent = len(overlap_list)/len(dwell_list)
    flight_list,l = process_flight(data)

    devn = statistics.stdev(flight_list)
    mean = statistics.mean(flight_list)
    covar = devn/mean
    wpm_brackets,recalculated_wpm = process_wpm_brackets(timing,text)
    dwell_mean = statistics.mean(dwell_times)
    dwell_std = statistics.stdev(dwell_times)

    if recalculated_wpm - wpm > 5 or recalculated_wpm - wpm < -5:
        result['bot'] = True
    if dwell_mean < 50:
        result['bot'] = True
    if covar < 0.1:
        result['bot'] = True
    if dwell_std > 500:
        result['bot'] = True

    result['wpm'] = wpm
    result['accuracy'] = len(text)/(len(text) + errors)
    result['dwell'] = dwell_mean
    result['flight'] = statistics.mean(flight_list)
    result['flightstd'] = statistics.stdev(flight_list)
    result['dwellstd'] = dwell_std
    result['overlap'] = overlap_percent
    result['covar'] = covar
    result['text'] = text
    result['key'] = str(uuid.uuid4())
    if 'bot' not in result:
        result['bot'] = False

    verbose_data['all_keys'] = data['all_keys']
    verbose_data['flight'] = data['flight']
    verbose_data['ku'] = data['ku']
    verbose_data['kd'] = data['kd']

    extra_data['brackets'] = wpm_brackets
    extra_data['keys_flight'] = l

    print(result)
    return ( True, wpm, result ,extra_data, verbose_data)

# imp params decreasing: overlap,  dwell stddev, dwell, flight,correct covar,
