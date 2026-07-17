param(
    [Parameter(Mandatory = $true)]
    [string]$SpritePath,

    [string]$PetId = "zhuchouta",
    [string]$DisplayName = "Zhuchouta",
    [string]$Description = "A tiny pig, otter, and tabby cat trio companion for Codex."
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $SpritePath)) {
    throw "找不到图集文件：$SpritePath"
}

$resolvedSpritePath = (Resolve-Path -LiteralPath $SpritePath).Path

if ($env:CODEX_HOME -and $env:CODEX_HOME.Trim()) {
    $codexHome = $env:CODEX_HOME
} else {
    $codexHome = Join-Path $HOME ".codex"
}

$petRoot = Join-Path $codexHome "pets"
$petDir = Join-Path $petRoot $PetId

New-Item -ItemType Directory -Force -Path $petDir | Out-Null

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$validatorPath = Join-Path $scriptDir "validate_spritesheet.py"

$pythonCommand = Get-Command python -ErrorAction SilentlyContinue

if ($pythonCommand -and (Test-Path -LiteralPath $validatorPath)) {
    & $pythonCommand.Source $validatorPath $resolvedSpritePath
    if ($LASTEXITCODE -ne 0) {
        throw "图集校验失败，安装已中止。"
    }
} else {
    Write-Host "未找到 python 或 validate_spritesheet.py，跳过自动校验。"
}

$targetSpritePath = Join-Path $petDir "spritesheet.webp"
Copy-Item -LiteralPath $resolvedSpritePath -Destination $targetSpritePath -Force

$manifestObject = [ordered]@{
    id = $PetId
    displayName = $DisplayName
    description = $Description
    spriteVersionNumber = 2
    spritesheetPath = "spritesheet.webp"
}

$manifestJson = $manifestObject | ConvertTo-Json -Depth 4
$manifestPath = Join-Path $petDir "pet.json"
[System.IO.File]::WriteAllText($manifestPath, $manifestJson, [System.Text.UTF8Encoding]::new($false))

Write-Host ""
Write-Host "Zhuchouta V2 安装完成。"
Write-Host "宠物目录：$petDir"
Write-Host "图集文件：$targetSpritePath"
Write-Host "清单文件：$manifestPath"
Write-Host ""
Write-Host "现在打开 Codex。"
Write-Host "进入 Settings > Appearance > Pets。"
Write-Host "选择 Zhuchouta，或在输入框输入 /pet 唤起宠物。"
