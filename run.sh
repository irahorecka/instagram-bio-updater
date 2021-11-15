# Bash script to execute main.py and main.js via cronjob on Raspberry Pi.
SHELL=/bin/bash

python /home/pi/Desktop/instagram-bio-updater/main.py && /usr/local/bin/node /home/pi/Desktop/instagram-bio-updater/main.js
