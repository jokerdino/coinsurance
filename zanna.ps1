# copy add.py and pivot-table.py to all directories here

$folders = Get-ChildItem -Directory;

ForEach ($folder in $folders.name) {
    Copy-Item add.py -Destination $folder
    Copy-Item pivot-table.py -Destination $folder
    cd $folder

    echo "Merging premium payable file and claims receivable file of $folder into one single file..."
    python add.py
    cd ..
} 

# all the combined files created by add.py python script will be saved in "doing" directory
# we are moving the files into the folder of the company using the same logic we used in the "sort.ps1" script


$allfiles = Get-ChildItem  | Where-Object {$_.PSisContainer -eq $false} | Select basename,fullname
foreach($file in $allfiles){
        $properfolder = Get-ChildItem  | Where-Object {$_.PSisContainer -eq $true -and $_.basename -match ($file.basename -split '_')[0]} | Select fullname
    TRY { move-item $file.fullname $properfolder.fullname  }
    CATCH { write-host "No matching folder was found."}
}

# now that we have a merged file, we will delete all the _premium and _claims file to avoid confusion

ForEach ($folder in $folders.name) {
    cd $folder
    Remove-Item *_Premium.xlsx
    Remove-Item *_Claims.xlsx

# time to use the pivot-table script to generate summary file for each company...
    echo "Generating summary file of $folder..."
    python pivot-table.py
    cd ..
}
   
