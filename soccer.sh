#!/bin/bash
pip_check=$(python -m pip --version)
if [[ $pip_check != *"/Library/Python"* ]]; then
  echo "Downloading and installing pip..."
  sudo su
  curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
  python get-pip.py
fi

python -c "import requests"
if [[ $? -ne 0 ]]; then
  echo "Downloading and installing python request library..."
  sudo pip install requests
fi

echo ""
python ./soccarena.py
echo ""
echo "----------------------------------------------------------------"
echo ""
python ./sv1880.py
