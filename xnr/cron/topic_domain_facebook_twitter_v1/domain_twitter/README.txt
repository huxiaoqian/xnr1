twitter账号没有类别信息，所以只能根据账号的个人描述识别身份

类别标签：
高校、境内媒体、境外媒体、境内组织、境外组织、法律机构及人士、政府机构及人士、媒体人士、活跃人士、商业人士、其他

对应的英文类别：
['university', 'admin', 'inner_admin', 'outer_admin', 'media', 'inner_media', 'outer_media','lawyer', 'politician', 'mediaworker', 'activer', 'other', 'business']

调用方法：from domain_classify import domain_main

输入数据：
user_data用户数据字典：{'uid':{'description':description,'username':username,'location':location,'number_of_text':number of text}...}
其中：
description:twitter用户背景信息中的description。注意：有部分内容是英文，需要转换成中文
username:twitter用户背景信息中的username
location:twitter用户背景信息中的location。注意：有部分内容是英文，需要转换成中文
number_of_text:用户最近7天发帖数量

输出数据：
user_label用户身份字典:{'uid':label,'uid':label...}


