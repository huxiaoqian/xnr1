# -*-coding: utf-8-*-
import sys
sys.path.append('..')

from sina.weibo_feedback_at import FeedbackAt
from sina.weibo_feedback_comment import FeedbackComment
from sina.weibo_feedback_follow import FeedbackFollow
from sina.weibo_feedback_like import FeedbackLike
from sina.weibo_feedback_private import FeedbackPrivate
from sina.weibo_feedback_retweet import FeedbackRetweet
from tools.Launcher import SinaLauncher


def execute(uname, upasswd):
    xnr = SinaLauncher(uname, upasswd)
    xnr.login()
    try:
        print 'start run weibo_feedback_at.py ...'
        FeedbackAt(xnr.uid).execute()
        print 'run weibo_feedback_at.py done!'

        print 'start run weibo_feedback_comment.py ...'
        FeedbackComment(xnr.uid).execute()
        print 'run weibo_feedback_comment.py done!'

        print 'start run weibo_feedback_follow.py ...'
        FeedbackFollow(xnr.uid).execute()
        print 'run weibo_feedback_follow.py done!'

        print 'start run weibo_feedback_like.py ...'
        FeedbackLike(xnr.uid).execute()
        print 'run weibo_feedback_like.py done!'

        print 'start run weibo_feedback_private.py ...'
        FeedbackPrivate(xnr.uid).execute()
        print 'run weibo_feedback_private.py done!'

        print 'start run weibo_feedback_retweet.py ...'
        FeedbackRetweet(xnr.uid).execute()
        print 'run weibo_feedback_retweet.py done!'
    except:
        print 'Except Abort'


if __name__ == '__main__':
    execute('', '')
