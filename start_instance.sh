apt update &&
apt install -y nginx &&
apt install -y firewalld &&
apt install -y pip &&
pip install Jinja2 &&
pip install gunicorn &&
git clone https://github.com/Tititun/architecture.git &&
sudo firewall-cmd --permanent --add-service=http && firewall-cmd --reload