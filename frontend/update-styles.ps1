# Script para actualizar estilos de dark mode a light mode en archivos TypeScript (.tsx)

$pagesPath = "C:\\Users\\veloz\\Desktop\\jci-proyecto\\frontend\\src"

# Patrones a reemplazar en todos los archivos TSX
$replacements = @(
    # Fondos oscuros a claros
    @{ Pattern = 'bg-dark-bg'; Replacement = 'bg-light-bg' },
    @{ Pattern = 'bg-dark-card'; Replacement = 'bg-light-card' },
    @{ Pattern = 'border-dark-border'; Replacement = 'border-light-border' },
    @{ Pattern = 'hover:bg-dark-bg'; Replacement = 'hover:bg-light-hover' },
    
    # Grises oscuros a claros/blancos
    @{ Pattern = 'bg-gray-900'; Replacement = 'bg-light-surface' },
    @{ Pattern = 'bg-gray-800([^/])'; Replacement = 'bg-white$1' },
    @{ Pattern = 'bg-gray-800/50'; Replacement = 'bg-white/80' },
    @{ Pattern = 'bg-gray-800/30'; Replacement = 'bg-white/50' },
    @{ Pattern = 'bg-gray-700'; Replacement = 'bg-neutral-50' },
    @{ Pattern = 'bg-gray-600'; Replacement = 'bg-neutral-200' },
    
    # Bordes oscuros a claros
    @{ Pattern = 'border-gray-700'; Replacement = 'border-light-border' },
    @{ Pattern = 'border-gray-600'; Replacement = 'border-neutral-300' },
    
    # Texto blanco a oscuro
    @{ Pattern = 'text-white([^/\-])'; Replacement = 'text-neutral-900$1' },
    @{ Pattern = 'text-white"'; Replacement = 'text-neutral-900"' },
    @{ Pattern = 'text-gray-400'; Replacement = 'text-neutral-600' },
    @{ Pattern = 'text-gray-300'; Replacement = 'text-neutral-700' },
    
    # Hovers oscuros a claros
    @{ Pattern = 'hover:text-white'; Replacement = 'hover:text-neutral-900' },
    @{ Pattern = 'hover:bg-gray-800'; Replacement = 'hover:bg-neutral-100' },
    @{ Pattern = 'hover:bg-gray-700'; Replacement = 'hover:bg-neutral-50' },
    @{ Pattern = 'hover:bg-gray-600'; Replacement = 'hover:bg-neutral-200' },
    
    # Placeholders
    @{ Pattern = 'placeholder-gray-400'; Replacement = 'placeholder-neutral-400' }
)

# Buscar todos los archivos .tsx en /pages y /components
$files = Get-ChildItem -Path $pagesPath -Filter "*.tsx" -Recurse -File

Write-Host "Encontrados $($files.Count) archivos .tsx" -ForegroundColor Cyan

$filesModified = 0

foreach ($file in $files) {
    $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
    $originalContent = $content
    
    foreach ($rep in $replacements) {
        $content = $content -replace $rep.Pattern, $rep.Replacement
    }
    
    if ($content -ne $originalContent) {
        Set-Content -Path $file.FullName -Value $content -Encoding UTF8 -NoNewline
        Write-Host "✓ Actualizado: $($file.FullName)" -ForegroundColor Green
        $filesModified++
    }
}

Write-Host "`n✅ Proceso completado!" -ForegroundColor Green
Write-Host "Archivos modificados: $filesModified de $($files.Count)" -ForegroundColor Yellow
