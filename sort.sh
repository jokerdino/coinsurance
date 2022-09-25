# create a folder called "to be processed
# if the file ends with premium.xlsx or claims.xlsx, move it to "to be processed" folder

# based on the names of the files before underscore, create a bunch of folders.

# move the files to the folders matching the name

echo "Creating folder named doing..."
mkdir doing

echo "Moving all premium payable files and claim receivable files to doing folder..."

for file in * ; do
   # file_name=`echo $file | awk -F_ '{print $2}'`
    #echo $(file_name)
    if [ "${file##*_}"  == Premium.xlsx ] ; then
        mv "$file" doing/
    elif [ "${file##*_}"  == Claims.xlsx ] ; then
        mv "$file" doing/
    fi
done
cd doing

echo "Creating folders for each company and moving each company specific payable and receivable files to that particular company's folder"
for file in * ; do
    dirname="${file%%_*}"
    mkdir -p "$dirname" 
    mv "$file" "$dirname"
done

cd ..

cp zanna.sh doing/
cp add.py doing/
cp pivot-table.py doing/

cd doing
