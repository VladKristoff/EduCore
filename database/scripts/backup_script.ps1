$DB_NAME = "educore_db"
$DB_USER = "postgres"
$env:PGPASSWORD = "1234"
$BACKUP_DIR = "C:\PostgreSQL\backups"
$TIMESTAMP = (Get-Date).ToString("yyyyMMdd_HHmmss")
$BACKUP_FILE = "$BACKUP_DIR\${DB_NAME}_$TIMESTAMP.backup"

$env:Path += ";E:\PostgreSQL\bin"

# 3. Создаем папку для бэкапов, если она отсутствует
if (!(Test-Path -Path $BACKUP_DIR)) {
    New-Item -ItemType Directory -Force -Path $BACKUP_DIR
}

Write-Host "Запуск резервного копирования базы данных $DB_NAME..."

# 4. Запуск pg_dump (теперь система точно знает, где лежит этот файл)
pg_dump.exe -U $DB_USER -F c -b -v -f $BACKUP_FILE $DB_NAME

# 5. Проверка результата
if ($LASTEXITCODE -eq 0) {
    Write-Host "Резервная копия успешно создана: $BACKUP_FILE" -ForegroundColor Green
} else {
    Write-Error "Ошибка при создании резервной копии!"
}