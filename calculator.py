
def calculate_cost(dbhelper, audience_size, channel_id_list, showbreakup):
    cost = 0
    range_info = []
    range_intervals = dbhelper.get_all_ranges()
    for id, start, end in range_intervals:
        if audience_size > 0:
            interval_size = end-start+1 if start != 0 else end-start
            range_info.append((id, min(interval_size, audience_size)))
            audience_size -= interval_size
    for channel_id in channel_id_list:
        channel_cost = 0
        if showbreakup:
            print("-------------------------------------------------")
            print('Channel : '+dbhelper.get_channel_name(channel_id))
        base_fee = dbhelper.get_base_fee(channel_id=channel_id)
        if showbreakup:
            print('Base Fee : $'+str(round(base_fee, 2))+' for ' +
                  str(range_info[0][1]) + ' users')
        cost += base_fee
        channel_cost += base_fee
        for range_id, size in range_info:
            trans_fee = dbhelper.get_trans_fee(
                range_id=range_id, channel_id=channel_id)
            if showbreakup:
                print('Transaction Fee : $'+str(round(trans_fee*size, 2)) +
                      ' for '+str(size)+' users')
            cost += size*trans_fee
            channel_cost += size*trans_fee
        if showbreakup:
            print("Total Channel Cost : $" + str(channel_cost))
            print("-------------------------------------------------")
    return cost
