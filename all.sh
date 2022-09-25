echo "Generating premium payable reports..."
python3 coinsurance.py

echo "Generating claims receivable reports..."
python3 claims.py
bash sort.sh
cd doing
bash zanna.sh

