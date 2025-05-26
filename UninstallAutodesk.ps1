Write-Host "Buscando productos de Autodesk instalados..." -ForegroundColor Cyan

$registryPaths = @(
    "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*",
    "HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*"
)

$autodeskProducts = @()

foreach ($path in $registryPaths) {
    Get-ItemProperty $path | Where-Object {
        $_.DisplayName -like "*Autodesk*" -and $_.UninstallString
    } | ForEach-Object {
        $product = @{
            Name = $_.DisplayName
            UninstallString = $_.UninstallString
        }
        $autodeskProducts += $product
    }
}

if ($autodeskProducts.Count -eq 0) {
    Write-Host "No se encontraron productos de Autodesk instalados." -ForegroundColor Yellow
    exit
}

Write-Host "Se encontraron los siguientes productos de Autodesk:" -ForegroundColor Green
$autodeskProducts | ForEach-Object { Write-Host " - $($_.Name)" }

$confirmation = Read-Host "¿Deseas forzar la desinstalación de todos estos productos? (s/n)"
if ($confirmation -ne "s") {
    Write-Host "Cancelado por el usuario." -ForegroundColor Red
    exit
}

foreach ($product in $autodeskProducts) {
    $uninstallCmd = $product.UninstallString
    Write-Host "`nProcesando: $($product.Name)" -ForegroundColor Cyan

    try {
        if ($uninstallCmd -match "msiexec\.exe.*\{.*\}") {
            if ($uninstallCmd -match "\{[0-9A-Fa-f\-]+\}") {
                $guid = $matches[0]
                Start-Process "msiexec.exe" -ArgumentList "/x $guid /quiet /norestart" -Wait
            }
        } else {
            Start-Process "cmd.exe" -ArgumentList "/c `"$uninstallCmd`"" -Wait
        }

        Write-Host "✔ Desinstalado: $($product.Name)" -ForegroundColor Green
    } catch {
        Write-Host "⚠ Error al desinstalar: $($product.Name)" -ForegroundColor Red
        Write-Host "Comando fallido: $uninstallCmd"
    }
}

Write-Host "`nProceso completado." -ForegroundColor Green
