FROM node:18-alpine

# Установка рабочей директории
WORKDIR /app

# Копирование package.json и package-lock.json
COPY package*.json ./

# Установка зависимостей
RUN npm ci

# Копирование исходного кода
COPY . .

# Открытие порта
EXPOSE 5173

# Команда по умолчанию
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"] 