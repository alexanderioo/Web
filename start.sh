#!/bin/bash

echo "🐎 Запуск системы управления конюшней с Docker..."

# Добавление Docker в PATH
export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"

# Проверка наличия Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Установите Docker Desktop: https://www.docker.com/products/docker-desktop"
    exit 1
fi

if ! command -v docker compose &> /dev/null; then
    echo "❌ Docker Compose не установлен."
    exit 1
fi

echo "✅ Docker найден"

# Остановка существующих контейнеров
echo "🛑 Остановка существующих контейнеров..."
docker compose down

# Сборка и запуск контейнеров
echo "🔨 Сборка и запуск контейнеров..."
docker compose up --build -d

# Ожидание запуска сервисов
echo "⏳ Ожидание запуска сервисов..."
sleep 10

# Проверка статуса контейнеров
echo "📊 Статус контейнеров:"
docker compose ps

echo ""
echo "🎉 Система запущена!"
echo ""
echo "🌐 Доступные сервисы:"
echo "   Django API:     http://localhost:8000"
echo "   React Frontend: http://localhost:5173"
echo "   Django Admin:   http://localhost:8000/admin"
echo "   Django Silk:    http://localhost:8000/silk/"
echo ""
echo "📝 Полезные команды:"
echo "   Просмотр логов: docker compose logs -f"
echo "   Остановка:      docker compose down"
echo "   Перезапуск:     docker compose restart"
echo "" 