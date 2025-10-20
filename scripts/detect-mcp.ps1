$candidateDirs = @(".\.claude\mcp", ".\mcp", ".\config\mcp")
$result = @()

foreach ($dir in $candidateDirs) {
  if (Test-Path $dir) {
    Get-ChildItem -Path $dir -Filter *.json -File -Recurse | ForEach-Object {
      try {
        $json = Get-Content $_.FullName -Raw | ConvertFrom-Json
        $name = if ($json.name) { $json.name } else { [System.IO.Path]::GetFileNameWithoutExtension($_.Name) }
        $result += [pscustomobject]@{
          name = $name
          path = $_.FullName
          raw  = $json
        }
      } catch { }
    }
  }
}

$result | Sort-Object -Property name -Unique | ConvertTo-Json -Depth 8
