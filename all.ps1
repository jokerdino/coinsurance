# running python script to generate premium payable

echo "Generating premium payable reports..."
python coinsurance.py

# running python script to generate claims receivable
echo "Generating claims receivable reports..."
python claims.py


./sort.ps1
cd doing
./zanna.ps1
