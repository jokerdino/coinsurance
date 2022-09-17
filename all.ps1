# running python script to generate premium payable

echo "Generating premium payable reports..."
python3 coinsurance.py

# running python script to generate claims receivable
echo "Generating claims receivable reports..."
python3 claims.py


./sort.ps1
echo "Moving to doing folder"
cd doing
./zanna.ps1
