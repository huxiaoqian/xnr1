pkill firefox
pkill geckodriver
pkill Xvfb
sleep 1
kill -9 $(ps -A -ostat,ppid | grep -e '[zZ]'| awk '{ print $2 }')
