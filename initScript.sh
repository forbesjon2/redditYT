
apt update
apt upgrade
apt update
apt install --assume-yes ffmpeg
apt install --assume-yes git
apt install --assume-yes vim 
apt install --assume-yes python3
apt install --assume-yes python3-pip
apt install --assume-yes cron
pip3 install imgkit
pip3 install boto3
pip3 install praw
pip3 install json
pip3 install numpy
pip3 install mutagen
pip3 install moviepy
pip3 install shutil
pip3 install requests
mkdir audo
mkdir video
mkdir output
mkdir img
mkdir data
git config --global user.email "forbesjon2@gmail.com"
git config --global user.name "forbesjon2"

echo "add this to cron"
echo "0 * * * * python3 /home/rboYT/main.py update >/dev/null 2>&1"
