facebook账号分个人账号和主页账号
个人账号可以创建主页，只有主页才有类别

类别标签：
高校、机构、媒体、民间组织、法律机构及人士、政府机构及人士、媒体人士、活跃人士、商业人士、其他

英文类别：
['university', 'admin', 'media', 'folkorg', 'lawyer', 'politician', 'mediaworker', 'activer', 'other', 'business']


调用方法：from domain_classify import domain_main

输入数据：
user_data用户数据字典：{'uid':{'bio_str':bio_string,'category':category,'number_of_text':number of text}...}
其中：
bio_str:Facebook用户背景信息中的quotes、bio、about、description，用'_'链接。注意：有部分内容是英文，需要转换成中文
category:Facebook用户背景信息中的category
number_of_text:用户最近7天发帖数量

输出数据：
user_label用户身份字典:{'uid':label,'uid':label...}



