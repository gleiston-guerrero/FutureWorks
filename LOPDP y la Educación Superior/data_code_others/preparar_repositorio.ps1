<#
.SYNOPSIS
    Separa el material publicable del que no debe subirse a un repositorio.

.DESCRIPTION
    Recorre la carpeta de trabajo y mueve a "No Subir" todo lo que contenga
    datos personales, material de terceros con licencia propia, respaldos
    comprimidos o artefactos de compilacion. Conserva la estructura de
    subcarpetas dentro de "No Subir" para que nada se mezcle.

    Por defecto solo informa. Para ejecutar los movimientos hay que pasar
    -Aplicar de forma explicita.

.EXAMPLE
    .\preparar_repositorio.ps1 -Raiz "C:\ruta\carpeta"
    .\preparar_repositorio.ps1 -Raiz "C:\ruta\carpeta" -Aplicar
#>
param(
    [Parameter(Mandatory = $true)][string]$Raiz,
    [switch]$Aplicar
)

$ErrorActionPreference = 'Stop'
$NoSubir = Join-Path $Raiz 'No Subir'

# --- Apellidos de las personas evaluadoras -------------------------------
$apellidos = 'taipe|figueroa|panama|tejada|pallo|carvajal|villamar|zamora|' +
             'castro|espinoza|fajardo|beltran|gaibor|farinango|moncayo|' +
             'escudero|alava|umaginga|pacheco|grefa|cruz|calle|rios|arias|' +
             'andrea|delgado'

# --- Reglas de exclusion, en orden de evaluacion -------------------------
$reglas = @(
    @{ n = 'Entregas de personas evaluadoras';   t = { param($f) $f.FullName -match '\\Evaluaciones\\' } },
    @{ n = 'Entregas dentro de Springer_UAIS';   t = { param($f) $f.FullName -match '\\\d+ Evaluaciones\\' } },
    @{ n = 'Nombre de persona en el archivo';    t = { param($f) $f.Name -match $apellidos } },
    @{ n = 'Clave de seudonimos';                t = { param($f) $f.Name -match 'NO_DEPOSITAR|clave_seudonimos' } },
    @{ n = 'Datos de validacion sin anonimizar'; t = { param($f) $f.Name -match '^validacion_manual_accesibilidad|^wcag_validacion_final|^validacion_manual_wcag' } },
    @{ n = 'Ranking de terceros con licencia';   t = { param($f) $f.Name -match 'QS World University|ShanghaiRanking|World University Rankings|Academic Ranking' } },
    @{ n = 'Respaldo comprimido';                t = { param($f) $f.Extension -match '^\.(zip|rar|7z)$' } },
    @{ n = 'Artefacto de compilacion LaTeX';     t = { param($f) $f.Extension -match '^\.(aux|log|out|bbl|blg|toc|lof|lot|fls|fdb_latexmk)$' -or $f.Name -match '\.synctex\.gz$' } },
    @{ n = 'Bitacora de trabajo';                t = { param($f) $f.Name -match '^ESTADO\.md$|^diagnostico_|^analisis_.*\.txt$' } },
    @{ n = 'Temporal de ofimatica';              t = { param($f) $f.Name -match '^~\$|^\.~lock' } },
    @{ n = 'Dependencias instalables';           t = { param($f) $f.FullName -match '\\node_modules\\' } },
    @{ n = 'Libro sin identificar';              t = { param($f) $f.Name -match '^Libro\d+\.xlsx$' } },
    @{ n = 'Informe de clasificacion';           t = { param($f) $f.Name -eq 'clasificacion_repositorio.csv' } }
)

if (-not (Test-Path $Raiz)) { throw "No existe la carpeta: $Raiz" }

$todos = Get-ChildItem $Raiz -Recurse -File -Force |
         Where-Object { $_.FullName -notmatch '\\\.git\\' -and $_.FullName -notmatch [regex]::Escape($NoSubir) }

$mover = @()
$quedan = @()
foreach ($f in $todos) {
    $motivo = $null
    foreach ($r in $reglas) {
        if (& $r.t $f) { $motivo = $r.n; break }
    }
    if ($motivo) { $mover += [pscustomobject]@{ Archivo = $f; Motivo = $motivo } }
    else         { $quedan += $f }
}

"Carpeta      : $Raiz"
"Archivos     : {0}" -f $todos.Count
"A No Subir   : {0}  ({1:N1} MB)" -f $mover.Count, (($mover.Archivo | Measure-Object Length -Sum).Sum / 1MB)
"Permanecen   : {0}  ({1:N1} MB)" -f $quedan.Count, (($quedan | Measure-Object Length -Sum).Sum / 1MB)
""
"--- Resumen por motivo ---"
$mover | Group-Object Motivo | Sort-Object Count -Descending |
    Select-Object @{n='motivo';e={$_.Name}},
                  @{n='archivos';e={$_.Count}},
                  @{n='MB';e={'{0:N1}' -f (($_.Group.Archivo | Measure-Object Length -Sum).Sum / 1MB)}} |
    Format-Table -AutoSize

# Informe completo para revisar antes de aplicar
$informe = Join-Path $Raiz 'clasificacion_repositorio.csv'
$mover | Select-Object @{n='ruta';e={$_.Archivo.FullName.Replace("$Raiz\","")}},
                       @{n='MB';e={'{0:N3}' -f ($_.Archivo.Length/1MB)}},
                       Motivo,
                       @{n='destino';e={'No Subir'}} |
    Export-Csv $informe -NoTypeInformation -Encoding UTF8
$quedan | Select-Object @{n='ruta';e={$_.FullName.Replace("$Raiz\","")}},
                        @{n='MB';e={'{0:N3}' -f ($_.Length/1MB)}},
                        @{n='Motivo';e={''}},
                        @{n='destino';e={'repositorio'}} |
    Export-Csv $informe -NoTypeInformation -Encoding UTF8 -Append

"Informe completo: $informe"
""

if (-not $Aplicar) {
    "SIMULACION. No se ha movido nada."
    "Revisa el informe y vuelve a ejecutar con -Aplicar para hacer efectivos los movimientos."
    return
}

New-Item -ItemType Directory -Force $NoSubir | Out-Null
$n = 0
foreach ($m in $mover) {
    $rel = $m.Archivo.FullName.Replace("$Raiz\", "")
    $dst = Join-Path $NoSubir $rel
    New-Item -ItemType Directory -Force (Split-Path $dst) | Out-Null
    Move-Item -LiteralPath $m.Archivo.FullName -Destination $dst -Force
    $n++
}
"Movidos: $n archivos a '$NoSubir'"

# Carpetas que quedaron vacias
Get-ChildItem $Raiz -Recurse -Directory -Force |
    Where-Object { $_.FullName -notmatch [regex]::Escape($NoSubir) } |
    Sort-Object { $_.FullName.Length } -Descending |
    ForEach-Object {
        if (-not (Get-ChildItem $_.FullName -Recurse -File -Force)) {
            Remove-Item $_.FullName -Recurse -Force
        }
    }
"Carpetas vacias eliminadas."
