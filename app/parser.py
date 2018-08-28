def process_list(ts_list):
    print(ts_list)
    timing = ts_list[1::2]
    wpm =  (len(timing)* 12)/ (timing[-1]/1000)
    wpm = round(wpm)
    diff = []
    for i in range(len(timing)-1):
        t = timing[i+1]-timing[i]
        if t < 0:
            return (False,)
        diff.append(t)
    import statistics
    devn = statistics.stdev(diff)
    devn = round(devn)
    if devn >= 50:
        return ( True, wpm, ts_list, devn)
    return (False,)
