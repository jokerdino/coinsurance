echo "Generating premium payable reports..."
python3 coinsurance.py
echo "Generating claims receivable reports..."
python3 claims.py

./sort.ps1
echo "Moving to doing folder"
cd doing
./zanna.ps1
