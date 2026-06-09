# restore_script.ps1

$DB_NAME = "educore_db"
$DB_USER = "postgres"
$BACKUP_DIR = "C:\PostgreSQL\backups"

$env:Path = "E:\PostgreSQL\bin;$env:Path"

# Показываем список доступных бэкапов
Write-Host "`nДоступные бэкапы:" -ForegroundColor Cyan
$backups = Get-ChildItem -Path $BACKUP_DIR -Filter "educore_db_*.backup" | Sort-Object LastWriteTime -Descending

if ($backups.Count -eq 0) {
    Write-Error "Нет бэкапов в папке $BACKUP_DIR"
    exit 1
}

for ($i = 0; $i -lt $backups.Count; $i++) {
    $b = $backups[$i]
    $size = [math]::Round($b.Length/1MB, 2)
    Write-Host "[$i] $($b.Name) - $($b.LastWriteTime) - ${size}MB"
}

# Выбор бэкапа
$index = Read-Host "`nВыберите номер бэкапа для восстановления"
if ($index -notmatch '^\d+$' -or $index -ge $backups.Count) {
    Write-Error "Неверный номер"
    exit 1
}

$backupFile = $backups[$index].FullName
Write-Host "Выбран бэкап: $backupFile" -ForegroundColor Yellow

# Запрос пароля
$password = Read-Host "Введите пароль пользователя $DB_USER" -AsSecureString
$env:PGPASSWORD = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password))

try {
    Write-Host "`nВосстановление базы данных..." -ForegroundColor Cyan
    
    # Завершаем соединения
    psql.exe -U $DB_USER -d postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '$DB_NAME' AND pid <> pg_backend_pid();" 2>$null
    
    # Удаляем старую БД
    psql.exe -U $DB_USER -d postgres -c "DROP DATABASE IF EXISTS $DB_NAME;" 2>$null
    
    # Создаем новую БД
    psql.exe -U $DB_USER -d postgres -c "CREATE DATABASE $DB_NAME WITH ENCODING='UTF8';" 2>$null
    
    # Восстанавливаем
    pg_restore.exe -U $DB_USER -d $DB_NAME -c --if-exists $backupFile
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ База данных успешно восстановлена!" -ForegroundColor Green
    } else {
        Write-Error "❌ Ошибка при восстановлении!"
    }
}
finally {
    $env:PGPASSWORD = ""
}