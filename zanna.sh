parentdir=$(pwd)

for d in ./*/ ; do
    mkdir -p "$d"/"$(basename "$d")"
    mv "$d"/*.xlsx "$d"/*/
    cp add.py "$d"/*/
    cp pivot-table.py "$d"/
done

for d in $parentdir/*/ ; do
    cd "$d"/"$(basename "$d")"
    printf '%s\n' "Merging premium payable file and claim receivable file into one single file... ${PWD##*/}"
    python3 add.py 
    rm add.py
    cd $parentdir 
done

for d in $parentdir/*/ ; do
    cd "$d"
    printf '%s\n' "Generating summary file - ${PWD##*/}"
    python3 pivot-table.py
    #rm pivot-table.py
    cd $parentdir
done
