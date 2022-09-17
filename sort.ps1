echo "creating folder named "doing"..."
New-Item -Name "doing" -ItemType "directory"

echo "Moving all premium payable files and claims receivable files to doing folder..."

Move-Item -Path * -Filter *_Premium.xlsx -Destination .\doing
Move-Item -Path * -Filter *_Claims.xlsx -Destination .\doing


Set-Location .\doing

$files = Get-ChildItem  -Filter *.xlsx -file;

echo "Creating folders for each company..."

ForEach ($file in $files) {
    $companies = ($file.BaseName -split '_')[0]

       $folder = New-Item -type directory -Force -Name $companies;
            
}

echo "Moving each company specific payable and receivable files to particular company's folder"

$allfiles = Get-ChildItem  | Where-Object {$_.PSisContainer -eq $false} | Select basename,fullname
foreach($file in $allfiles){
        $properfolder = Get-ChildItem  | Where-Object {$_.PSisContainer -eq $true -and $_.basename -match ($file.basename -split '_')[0]} | Select fullname
    TRY { move-item $file.fullname $properfolder.fullname  }
    CATCH { write-host "No matching folder was found."}
}


cd -


Copy-Item add.py -Destination .\doing
Copy-Item pivot-table.py -Destination .\doing
Copy-Item zanna.ps1 -Destination .\doing
