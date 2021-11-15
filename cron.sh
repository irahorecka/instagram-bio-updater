
#!/usr/bin/env bash

crontab -l > mycron
# Setup cron headers
echo "SHELL=/bin/bash" >> mycron
# For executing updating IG bio every hour every day.
echo "0 */1 * * * source ~/.bashrc && source /home/pi/instagram-bio-updater/venv/bin/activate && bash run.sh" >> mycron
crontab mycron
rm mycron
