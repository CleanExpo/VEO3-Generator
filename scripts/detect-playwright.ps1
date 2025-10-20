# Detect Playwright presence & key paths
$exists = $false
$pkgPath = Join-Path (Get-Location) "package.json"
if (Test-Path $pkgPath) {
  try {
    $pkg = Get-Content $pkgPath -Raw | ConvertFrom-Json
    $exists = ($pkg.dependencies.playwright -or $pkg.devDependencies.playwright `
            -or $pkg.dependencies."@playwright/test" -or $pkg.devDependencies."@playwright/test")
  } catch { $exists = $false }
}

$summary = @{
  hasPlaywright = $exists
  configFiles   = @()
  testDirs      = @()
}

Get-ChildItem -Recurse -File -Include "playwright.config.*" -ErrorAction SilentlyContinue | ForEach-Object {
  $summary.configFiles += $_.FullName
}
Get-ChildItem -Recurse -Directory -Include "tests","e2e","playwright" -ErrorAction SilentlyContinue | ForEach-Object {
  if ($_.FullName -match "(?i)(tests\\e2e|playwright)") { $summary.testDirs += $_.FullName }
}

$summary | ConvertTo-Json -Depth 5
