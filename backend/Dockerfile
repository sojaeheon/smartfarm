# Python 이미지 사용
FROM python:3.12.3

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 파일 복사
COPY . /app

RUN mkdir -p /app/.cache/huggingface && chmod -R 777 /app/.cache

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 6000

# uWSGI 실행
CMD ["uwsgi", "--ini", "uwsgi.ini"]