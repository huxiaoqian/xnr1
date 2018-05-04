#-*- coding: utf-8 -*-
import os
import smtplib
import mimetypes
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def send_mail(from_user, to_user, content):
    msg = MIMEMultipart()
    to_user_addr = to_user['addr'].split(',')
    msg['From'] = _format_addr('%s <%s>' % (from_user['name'].decode('utf8'), from_user['addr']) )
    msg['To'] = _format_addr('%s <%s>' % (to_user['name'].decode('utf8'), to_user_addr) )
    msg['Subject'] = Header(content['subject'].decode('utf8'))

    files_path = content.get('files_path')
    cid = []
    if files_path:
        files_path_list = files_path.split(',')
        for i in range(len(files_path_list)):
            filepath = files_path_list[i]
            filename = os.path.basename(filepath)
            filetype = mimetypes.guess_type(filepath)[0].split('/')
            with open(filepath, 'rb') as f:
                if filetype[0] == 'image': #标记图片的index，以便在网页中插入图片
                    cid.append((i, 1))
                else:
                    cid.append((i, 0))
                # 设置附件的MIME和文件名
                mime = MIMEBase(filetype[0] , filetype[1], filename=filename)
                # 加上必要的头信息:
                mime.add_header('Content-Disposition', 'attachment', filename=filename)
                mime.add_header('Content-ID', '<'+ str(i) +'>')
                mime.add_header('X-Attachment-Id', str(i))
                # 把附件的内容读进来:
                mime.set_payload(f.read())
                # 用Base64编码:
                encoders.encode_base64(mime)
                # 添加到MIMEMultipart:
                msg.attach(mime)

    html = '<html><body><h1>'+ content['text'] +'</h1>' 
    for index,flag in cid:
        if flag :
            html += '<p><img src="cid:%s"></p>' % str(index)
    html += '</body></html>'
    msg.attach(MIMEText(html, 'html', 'utf-8'))

    try:
        server = smtplib.SMTP_SSL(from_user['smtp_server'], 465)
        server.login(from_user['addr'], from_user['password'])
        server.sendmail(from_user['addr'], to_user_addr, msg.as_string())
        server.quit()
        return 1
    except Exception,e:
        print e
        return 0

if __name__ == '__main__':
    content = {
        'subject': '扫描二维码以登陆微信虚拟人',
        'text': '当前微信虚拟人【duolahanbao】【已掉线】，请管理员及时扫码进行登陆，以免影响业务谢谢。',
        'files_path': '/home/ubuntu8/hanmc/666/xnr1/xnr/static/WX/WXXNR0006_c090d97d406a16b461889d6526235d58_qrcode.png',	#支持多个，以逗号隔开
        }
    from_user = {
        'name': '虚拟人项目（微信）',
        'addr': '929673096@qq.com',
        'password': 'czlasoaiehchbega',
        'smtp_server': 'smtp.qq.com'   
    }
    to_user = {
        'name': '管理员',
        'addr': '929673096@qq.com'  #支持多个，以逗号隔开
    }
    print send_mail(from_user=from_user, to_user=to_user, content=content)
