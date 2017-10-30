#-*-coding:utf-8-*-

def user_no2wxbot_id(user_no):
    task_id = 'WXXNR'+str('%04d'%user_no)  #五位数 QXNR0001
    return task_id

def wxbot_id2user_no(task_id):
    user_no_string = filter(str.isdigit,task_id)
    user_no = int(user_no_string)
    return user_no

def string_md5(str):
    md5 = ''
    if type(str) is types.StringType:
        _md5 = hashlib.md5()
        _md5.update(str)
        md5 = _md5.hexdigest()
    return md5
    
if __name__ == '__main__':
    print user_no2wxbot_id(1)