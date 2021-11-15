
#!/usr/bin/env bash

crontab -l > mycron
# Setup cron headers
echo "SHELL=/bin/bash" >> mycron
# For executing updating IG bio every 30 minutes every day on the RaspberryPi.
echo "*/30 * * * * source /home/pi/Desktop/instagram-bio-updater/venv/bin/activate && bash /home/pi/Desktop/instagram-bio-updater/run.sh >> /home/pi/Desktop/cron-errorlog.txt 2>&1" >> mycron
crontab mycron
rm mycron
