ps -ef|grep cloud_monitor_server|grep -v grep|cut -c 9-15|xargs kill -9

