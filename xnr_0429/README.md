# xnr1
=== === === === === === =项目启动方式= === === === === === === === === === === === ===

启动
/home/xnr1/xnr_0429/xnr  下
supervisord -c supervisord.config 【】===启动

supervisorctl -c supervisord.config === 进入 supervisor  == 可以start run     stop run  开关端口

exit() 退出

:
pkill supervisorctl
:
pkill supervisord
:
pkill supervisor

查看 supervisord 是否在运行：
ps aux | grep supervisord

=============一些配置文件地址==========
[uwsgi] xnr/config.ini
[supervisor] xnr/supervisord.config 
