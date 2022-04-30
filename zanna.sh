parentdir=$(pwd)

for d in ./*/ ; do
    mkdir -p "$d"/"$(basename "$d")"
    mv "$d"/*.xlsx "$d"/*/
    cp add.py "$d"/*/
    cp pivot-table.py "$d"/
done

for d in $parentdir/*/ ; do
    cd "$d"/"$(basename "$d")"
    python3 add.py 
    rm add.py
    cd $parentdir 
done

for d in $parentdir/*/ ; do
    cd "$d"
    python3 pivot-table.py
    #rm pivot-table.py
    cd $parentdir
done
