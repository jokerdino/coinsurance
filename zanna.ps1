# copy add.py and pivot-table.py to all directories here

$folders = Get-ChildItem -Directory;

ForEach ($folder in $folders.name) {
    Copy-Item add.py -Destination $folder
    Copy-Item pivot-table.py -Destination $folder
    cd $folder
    python3 add.py
    cd -
} #   NewItem -Name $folder -ItemType -directory
    #Move-Item *.xlsx $folder
    #MoveItem add.py $folder
    #cd -
#Copy-Item pivot-table.py -Destination $folder



$allfiles = Get-ChildItem  | Where-Object {$_.PSisContainer -eq $false} | Select basename,fullname
foreach($file in $allfiles){
        $properfolder = Get-ChildItem  | Where-Object {$_.PSisContainer -eq $true -and $_.basename -match ($file.basename -split '_')[0]} | Select fullname
    TRY { move-item $file.fullname $properfolder.fullname  }
    CATCH { write-host "No matching folder was found."}
}

ForEach ($folder in $folders.name) {
    cd $folder
    Remove-Item *_Premium.xlsx
    Remove-Item *_Claims.xlsx
    echo $folder
    python3 pivot-table.py
    cd -
}
   
    Remove-Item *.xlsx
# Move-Item add.py -Destination $properfolder
   # cd $properfolder
   # python3 add.py
    
    #cd -
    #cd -

#}
