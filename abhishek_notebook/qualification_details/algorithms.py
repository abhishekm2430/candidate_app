def max_subarray(arr):
    st, ma = 0, 0
    curr_st, curr_ma = 0, 0
    for i in range(len(arr) - 1):
        if (arr[i+1] - arr[i]) < 7:
            if(curr_ma < ((i - curr_st) + 1)):
                curr_ma = ((i - curr_st) + 1)
        else:
            if(curr_ma > ma):
                ma = curr_ma
                st = curr_st
            curr_st = i + 1

    if(curr_ma > ma):
        ma = curr_ma
        st = curr_st

    end_point = st + ma + 1
    result = arr[st:end_point]
    return result









