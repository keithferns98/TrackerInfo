from dateutil.parser import isoparse


def filter_isodatetime_from_dict(data, start_dt, end_dt):
    filtered_data = []
    for curr_data in data:
        if start_dt <= curr_data["sts"] <= end_dt:
            curr_data["location"] = (curr_data["lat"], curr_data["long"])
            del curr_data["lat"]
            del curr_data["long"]
            filtered_data.append(curr_data)
    return filtered_data
