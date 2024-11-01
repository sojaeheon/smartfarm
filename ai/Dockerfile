# Stage 1: CUDA와 cuDNN이 포함된 NVIDIA 이미지 사용
#FROM nvidia/cuda:12.6.2-runtime-ubuntu24.04 AS base

FROM python:3.12.3

# 작업 디렉토리 설정
WORKDIR /workspace

# 필요한 파일 복사
COPY . /workspace

# 필요한 패키지 설치 (Python, 폰트 및 fontconfig 설치)
RUN apt-get update && apt-get install -y \
    fonts-nanum \
    fontconfig \
    && apt-get clean

# 폰트 캐시 업데이트
RUN fc-cache -fv

# 권한 설정
RUN chmod -R 777 /workspace/chroma_db

# 의존성 설치 (requirements.txt 사용)
RUN pip install --no-cache-dir -r requirements.txt

# Hugging Face 관련 디렉토리 및 권한 설정
RUN mkdir -p /home/aim/.cache/huggingface && chmod -R 777 /home/aim/.cache

# 환경 변수 설정
ENV HF_TOKEN="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"
ENV HF_HOME="/home/aim/.cache/huggingface"
ENV TRANSFORMERS_CACHE="/home/aim/.cache/huggingface/hub"

# 포트 노출
EXPOSE 7777

# uWSGI 실행
CMD ["uwsgi", "--ini", "uwsgi.ini"]