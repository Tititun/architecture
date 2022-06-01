apt update &&
apt install -y nginx &&
apt install -y firewalld &&
apt install -y pip &&
git clone https://github.com/Tititun/architecture.git &&
pip install -r architecture/requirements.txt &&
sudo firewall-cmd --permanent --add-service=http && firewall-cmd --reload