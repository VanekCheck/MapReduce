
def flatten_array(arr):
    flattened_arr = []
    for sub_arr in arr:
        for item in sub_arr:
            flattened_arr.append(item)
    return flattened_arr


def remove_duplicates(arr):
    final_list = []
    for num in arr:
        if num not in final_list:
            final_list.append(num)
    return final_list


