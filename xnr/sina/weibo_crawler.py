# -*-coding: utf-8-*-
import time
import sys
sys.path.append('..')

from sina.weibo_feedback_at import FeedbackAt
from sina.weibo_feedback_comment import FeedbackComment
from sina.weibo_feedback_follow import FeedbackFollow
from sina.weibo_feedback_like import FeedbackLike
from sina.weibo_feedback_private import FeedbackPrivate
from sina.weibo_feedback_retweet import FeedbackRetweet
from tools.Launcher import SinaLauncher

def newest_time_func():
    

def execute(uname, upasswd):

    xnr = SinaLauncher(uname, upasswd)
    xnr.login()
    current_ts = int(time.time())
    try:
        print 'start run weibo_feedback_follow.py ...'
        fans, follow, groups = FeedbackFollow(xnr.uid, current_ts).execute()
        print 'run weibo_feedback_follow.py done!'
        
        print 'start run weibo_feedback_at.py ...'
        FeedbackAt(xnr.uid, current_ts, fans, follow).execute()
        print 'run weibo_feedback_at.py done!'

        print 'start run weibo_feedback_comment.py ...'
        FeedbackComment(xnr.uid, current_ts, fans, follow).execute()
        print 'run weibo_feedback_comment.py done!'

        print 'start run weibo_feedback_like.py ...'
        FeedbackLike(xnr.uid, current_ts, fans, follow).execute()
        print 'run weibo_feedback_like.py done!'

        print 'start run weibo_feedback_private.py ...'
        FeedbackPrivate(xnr.uid, current_ts, fans, follow).execute()
        print 'run weibo_feedback_private.py done!'

        print 'start run weibo_feedback_retweet.py ...'
        FeedbackRetweet(xnr.uid, current_ts, fans, follow).execute()
        print 'run weibo_feedback_retweet.py done!'
        
    except:
        print 'Except Abort'


if __name__ == '__main__':
    execute('weiboxnr02@126.com','xnr123456')
