python3 -m venv .venv_web3
source .venv_web3/bin/activate
python3 -m pip install -r requirements.txt
echo "PRIVATE_KEY=<>" >> .env
echo "Do replace <> with the actual private key..."
