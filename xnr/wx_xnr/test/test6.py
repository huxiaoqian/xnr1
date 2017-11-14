

def _id2user_no(task_id):
    user_no_string = filter(str.isdigit,task_id)
    #print 'user_no_string::',user_no_string
    user_no = int(user_no_string)
    #print 'user_no::',user_no
    return user_no

print _id2user_no('WXXNR0001')