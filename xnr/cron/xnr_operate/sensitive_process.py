# -*-coding:utf-8-*-

from DFA_filter import createWordTree,searchWord 


from parameter import RUN_TYPE, RUN_TEST_TIME, DAY,sensitive_score_dict
from global_config import SENSITIVE_WORDS_PATH
from global_utils import R_ADMIN as r_sensitive


def sensitive_process(text,timestamp):
	item = dict()

	DFA = createWordTree()
	sensitive_words_dict = searchWord(text.encode('utf-8', 'ignore'), DFA)
	if sensitive_words_dict:
        item['sensitive_words_string'] = "&".join(sensitive_words_dict.keys())
        item['sensitive_words_dict'] = json.dumps(sensitive_words_dict)
    else:
        item['sensitive_words_string'] = ""
        item['sensitive_words_dict'] = json.dumps({})

    #timestamp = item['timestamp']
    date = ts2datetime(timestamp)
    ts = datetime2ts(date)

    if sensitive_words_dict:
        print sensitive_words_dict.keys()[0]
        sensitive_count_string = r_cluster.hget('sensitive_'+str(ts), str(uid))
        if sensitive_count_string: #redis取空
            sensitive_count_dict = json.loads(sensitive_count_string)
            for word in sensitive_words_dict.keys():
                if sensitive_count_dict.has_key(word):
                    sensitive_count_dict[word] += sensitive_words_dict[word]
                else:
                    sensitive_count_dict[word] = sensitive_words_dict[word]
            r_cluster.hset('sensitive_'+str(ts), str(uid), json.dumps(sensitive_count_dict))
        else:
            r_cluster.hset('sensitive_'+str(ts), str(uid), json.dumps(sensitive_words_dict))



    sensitive_words_dict = json.loads(item['sensitive_words_dict'])
        if sensitive_words_dict:
            score = 0
            for k,v in sensitive_words_dict.iteritems():
                tmp_stage = r_sensitive.hget("sensitive_words", k)
                if tmp_stage:
                    score += v*sensitive_score_dict[str(tmp_stage)]
            index_body['sensitive'] = score