# Build 단계
FROM node:18-alpine AS build-stage

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 설치
COPY package*.json ./
RUN npm install

# 소스 복사 및 빌드
COPY . .
RUN npm run build

# Production 단계
FROM nginx:alpine AS production-stage

# 빌드된 파일 복사
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Nginx 설정 복사
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Nginx 실행
CMD ["nginx", "-g", "daemon off;"]