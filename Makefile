
PROJECT_DIR='/home/isan/Desktop/random/ubuntu-indicator-k8s/k8s-cluster-switcher-ubuntu-indicator'
all: 
	pip3 install -r requirements.txt
	sed 's!@!"${PROJECT_DIR}!' K8sSwitcher.desktop >> ${HOME}/.config/autostart/K8sSwitcher.desktop