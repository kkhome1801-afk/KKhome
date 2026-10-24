<#
.SYNOPSIS
    Tự động đồng bộ, kéo (pull) và đẩy (push/deploy) mã nguồn Git sử dụng GitHub Personal Access Token lưu trong file .env.
.DESCRIPTION
    Script đọc GITHUB_TOKEN từ file .env tại thư mục gốc và tự động cấu hình URL git remote origin.
.EXAMPLE
    .\scripts\git-sync.ps1 -Pull
    .\scripts\git-sync.ps1 -Push -Message "Cập nhật tính năng mới"
    .\scripts\git-sync.ps1 -Deploy -Message "Deploy phiên bản mới"
#>

[CmdletBinding()]
param (
    [switch]$Pull,
    [switch]$Push,
    [switch]$Deploy,
    [switch]$SyncRemote,
    [string]$Message = "Auto update code $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')",
    [string]$Branch = ""
)

# 1. Tìm đường dẫn thực thi Git
$gitCmd = "git"
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    $candidatePaths = @(
        "C:\Program Files\Git\cmd\git.exe",
        "C:\Program Files\Git\bin\git.exe",
        "$env:LOCALAPPDATA\Programs\Git\cmd\git.exe",
        "C:\Program Files (x86)\Git\cmd\git.exe"
    )
    foreach ($candidate in $candidatePaths) {
        if (Test-Path $candidate) {
            $gitCmd = $candidate
            $env:Path = "$([System.IO.Path]::GetDirectoryName($candidate));$env:Path"
            break
        }
    }
}

if (-not (Get-Command $gitCmd -ErrorAction SilentlyContinue) -and -not (Test-Path $gitCmd)) {
    Write-Error "Khong tim thay Git tren he thong. Vui long cai dat Git!"
    exit 1
}

$rootDir = Split-Path -Parent $PSScriptRoot
if (-not $rootDir) { $rootDir = Get-Location }

$envPath = Join-Path $rootDir ".env"
if (-not (Test-Path $envPath)) {
    Write-Error "Khong tim thay file .env tai $envPath! Vui long tao file .env va dien GITHUB_TOKEN."
    exit 1
}

# Đọc cấu hình từ .env
$envConfig = @{}
Get-Content $envPath | ForEach-Object {
    $line = $_.Trim()
    if ($line -and -not $line.StartsWith("#")) {
        $parts = $line -split "=", 2
        if ($parts.Length -eq 2) {
            $key = $parts[0].Trim()
            $value = $parts[1].Trim().Trim('"').Trim("'")
            $envConfig[$key] = $value
        }
    }
}

$token = $envConfig["GITHUB_TOKEN"]
$username = if ($envConfig["GITHUB_USERNAME"]) { $envConfig["GITHUB_USERNAME"] } else { "kkhome1801-afk" }
$repo = if ($envConfig["GITHUB_REPO_NAME"]) { $envConfig["GITHUB_REPO_NAME"] } else { "KKhome" }
if (-not $Branch) {
    $Branch = if ($envConfig["DEPLOY_BRANCH"]) { $envConfig["DEPLOY_BRANCH"] } else { "main" }
}

if (-not $token) {
    Write-Error "Bien GITHUB_TOKEN chua duoc thiet lap trong file .env!"
    exit 1
}

# Đảm bảo thông tin user git được thiết lập
$currentUserName = & $gitCmd config user.name
if (-not $currentUserName) {
    & $gitCmd config user.name "$username"
}
$currentUserEmail = & $gitCmd config user.email
if (-not $currentUserEmail) {
    & $gitCmd config user.email "${username}@users.noreply.github.com"
}

# Cập nhật Git Remote URL với Token
$authenticatedUrl = "https://${token}@github.com/${username}/${repo}.git"
& $gitCmd remote set-url origin $authenticatedUrl
Write-Host "-> Da cap nhat remote origin voi Token tu .env thanh cong." -ForegroundColor Green

if ($SyncRemote) {
    Write-Host "Da dong bo Git Remote URL. Ket thuc." -ForegroundColor Cyan
    exit 0
}

# Xử lý lệnh Pull
if ($Pull) {
    Write-Host "Dang thuc hien git pull origin $Branch..." -ForegroundColor Yellow
    & $gitCmd pull origin $Branch
    if ($LASTEXITCODE -eq 0) {
        Write-Host "-> Pull thanh cong tu origin/$Branch!" -ForegroundColor Green
    } else {
        Write-Host "-> Loi khi pull code." -ForegroundColor Red
        exit $LASTEXITCODE
    }
}

# Xử lý lệnh Push hoặc Deploy
if ($Push -or $Deploy) {
    if ($Deploy) {
        Write-Host "Dang kiem tra truoc khi deploy..." -ForegroundColor Yellow
        if (Test-Path (Join-Path $rootDir "package.json")) {
            Write-Host "Kiem tra cu phap va lint..." -ForegroundColor Yellow
            npm run lint
            if ($LASTEXITCODE -ne 0) {
                Write-Host "Canh bao: Lint co loi, vui long kiem tra truoc khi deploy!" -ForegroundColor Magenta
            }
        }
    }

    Write-Host "Dang chuan bi commit va push len $Branch..." -ForegroundColor Yellow
    & $gitCmd add -A
    
    # Kiểm tra xem có thay đổi để commit không
    $status = & $gitCmd status --porcelain
    if ($status) {
        & $gitCmd commit -m "$Message"
        if ($LASTEXITCODE -ne 0) {
            Write-Host "-> Loi khi commit thay doi." -ForegroundColor Red
            exit $LASTEXITCODE
        }
        Write-Host "-> Da commit thay doi: '$Message'" -ForegroundColor Green
    } else {
        Write-Host "Khong co thay doi moi can commit. Dang kiem tra push..." -ForegroundColor Cyan
    }

    Write-Host "Dang push len origin $Branch..." -ForegroundColor Yellow
    & $gitCmd push origin $Branch
    if ($LASTEXITCODE -eq 0) {
        Write-Host "-> Push/Deploy thanh cong len branch origin/$Branch!" -ForegroundColor Green
    } else {
        Write-Host "-> Loi khi push len origin." -ForegroundColor Red
        exit $LASTEXITCODE
    }
}

if (-not $Pull -and -not $Push -and -not $Deploy -and -not $SyncRemote) {
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host " Git & Deploy Helper with .env Token" -ForegroundColor Cyan
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host " Cach dung:"
    Write-Host "   .\scripts\git-sync.ps1 -Pull                       # Keo code moi nhat ve"
    Write-Host "   .\scripts\git-sync.ps1 -Push -Message 'Noi dung'  # Commit va day code len"
    Write-Host "   .\scripts\git-sync.ps1 -Deploy -Message 'Deploy'  # Kiem tra & Day len main"
    Write-Host "   .\scripts\git-sync.ps1 -SyncRemote                 # Dong bo token vao remote"
    Write-Host "==========================================================" -ForegroundColor Cyan
}
