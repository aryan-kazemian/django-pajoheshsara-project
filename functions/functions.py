def make_grope(items: list, grope_size):
    groped_list = []
    items = items[::-1]
    for i in range(0, len(items), grope_size):
        grop = items[i:i + grope_size]
        groped_list.append(grop)
    return groped_list


def compare_date_time(dt1, dt2):
    year1 = dt1[:4]
    year2 = dt2[:4]
    month1 = dt1[5:7]
    month2 = dt2[5:7]
    day1 = dt1[8:10]
    day2 = dt2[8:10]
    h1 = dt1[11:13]
    h2 = dt2[11:13]
    m1 = dt1[14:16]
    m2 = dt2[14:16]
    s1 = dt1[17:19]
    s2 = dt2[17:19]
    if year1 > year2:
        return dt1
    elif year2 > year1:
        return dt2
    else:
        if month1 > month2:
            return dt1
        elif month2 > month1:
            return dt2
        else:
            if day1 > day2:
                return dt1
            elif day2 > day1:
                return dt2
            else:
                if h1 > h2:
                    return dt1
                elif h2 > h1:
                    return dt2
                else:
                    if m1 > m2:
                        return dt1
                    elif m2 > m1:
                        return dt2
                    else:
                        if s1 > s2:
                            return dt1
                        elif s2 > s1:
                            return dt2
                        else:
                            return dt2


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip