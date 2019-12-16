sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3.8
alias python=python3.8
alias python3=python3.8
alias pip=pip3

pip install pillow
pip install matplotlib
pip install numpy
pip install lidar

sudo cp robot.service /etc/systemd/system/robot.service
sudo systemctl start robot.service
sudo systemctl enable robot.service
