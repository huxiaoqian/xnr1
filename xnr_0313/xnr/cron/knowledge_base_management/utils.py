# -*-coding:utf-8-*-

def split_city(geo):
    geo = geo.split('&')
    if geo[0] == '中国':
        province = geo[1]
        try:
            city = geo[2]
        except:
            city = 'unknown'
    else:
        province = 'unknown'
        city = 'unknown'
    return province,city