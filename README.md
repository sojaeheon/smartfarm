# 조명은 LED - Smartfarm

## 조원
* 하승철
* 박현준
* 소재헌
* 최유정
* 하령경

## 노션
조명은 LED - (https://www.notion.so/daa597b71e6b46b9a22b0299711b95e0)

# 시스템 구성
![image](https://github.com/user-attachments/assets/87ff1455-ecf9-455d-9cf2-60fc420a8734)
<br/>

# 주요 기능
### 1. 로그인
#### 1.1 사용자 로그인

### 2. 메인
#### 2.1 실시간 환경 센서값 및 환경 그래프
#### 2.2 엑츄에이터 작동
#### 2.3 일기예보 API

### 3. 병해진단페이지
#### 3.1 사진을 넣거나 찍어서 병해 확인

### 4. 챗봇페이지
#### 4.1 질문에 대한 답변을 얻을 수 있음
<br/><br/>

# 프로젝트 서버
### WSL2
  -  Windows에서 리눅스 커널을 가상화하여 리눅스 환경을 제공
  -  기존의 VM과 달리 WSL2는 훨씬 더 가볍고 빠름
  -  Docker는 본래 리눅스 기반으로 개발되었기 때문에, Windows에서 도커를 원활하게 사용하려면 WSL2가 필요
### Nginx
  - 리버스 프록시와 정적 파일 서비스를 제공하고, 트래픽 관리 및 부하 분산 기능을 담당하기 위해 사용
  - 빠르고 가벼운 웹 서버 동적인 것은 Flask로 보내고, 정적 파일들을 제공하여 서버 부하를 줄임
### uWSGI
  -  Flask와 같은 Python 웹 애플리케이션을 Nginx와 연결하기 위해 사용
  -   다중 프로세스 및 다중 스레드로 애플리케이션을 실행할 수 있음
### Flask
  - Python 기반의 경량 웹 프레임워크로, 간단하고 빠르게 웹 애플리케이션을 구축할 수 있음
  - 유연성과 확장성이 뛰어남
### Vue
  - 프론트엔드 사용자 인터페이스(UI)를 구축하고, 동적인 사용자 경험을 제공
### MySQL
  - 데이터의 저장 및 관리를 위해 사용
  - 프로젝트에서는 ai, sensor, disease 테이블에 각 해당 데이터를 저장
### Docker
  -  애플리케이션을 컨테이너(Container) 라는 격리된 환경에 배포하고 실행할 수 있게 해주는 플랫폼
![도커 컨테이너](https://github.com/user-attachments/assets/47da0289-d223-4602-b4bf-554f58870afe)

  - 각 이미지
    #### 1. ai image
      - AI 기능을 처리하는 서버로, 질병 진단과 같은 AI 관련 작업을 수행
      - Flask, Huggingface, uWSGI 등 사용
    #### 2. frontend image
      - Vue.js를 기반으로 하며, 사용자에게 UI를 제공하고 AI 서버 및 백엔드 서버와 통신하여 데이터를 표시
    #### 3. backend image
      - Flask 기반의 백엔드 서버로, 데이터베이스와 통신하며 사용자 요청을 처리합니다. AI 서버와 프론트엔드 간의 데이터         흐름을 관리
      - Flask, uWSGI등을 사용
    #### 4. Nginx image
      - 리버스 프록시 역할을 하는 Nginx 서버로, 모든 HTTP 요청을 프론트엔드, 백엔드 및 AI 서버로 라우팅
      - 배포된 이미지를 사용
<br/><br/>
# 스마트팜
![image](https://github.com/user-attachments/assets/01ae0753-3ec2-4c1b-b5b5-b784f1da6162)
- 라즈베리파이4 이용
- 액츄에이터 : DC팬, 워터펌프, 생장형 LED
- 센서 : 조도, CO2, 온도, 습도, 수위 
<br/><br/>

# 로그인
## 로그인 및 회원가입 화면
### 로그인 
![image](https://github.com/user-attachments/assets/26b8a7e8-da9c-4293-bffe-abfd02687b35)
### 회원가입
![image](https://github.com/user-attachments/assets/5de2f255-75a1-4a2c-9d2a-69975d31c39b)
  - 사용자의 id, password, 라즈베리파이 디바이스 정보를 데이터베이스에 저장
<br/><br/>

# 메인
## 메인 화면
![image](https://github.com/user-attachments/assets/c6c89a22-b682-4194-ac22-fc3184ce29b3)
### 카메라
  - 라즈베리파이에 카메라를 달아 실시간 스트리밍

### 액츄에이터
  - HTTP통신을 통한 액츄에이터 작동

### 환경 그래프
  - 환경 그래프를 통한 스마트팜 내부의 센서값 확인

### 시간별 날씨 정보 확인
  - Openweather에서 API를 사용 
<br/><br/>

# 병해진단
## Roboflow 이용
### 1. 모델 : Roboflow 3.0 Object Detection (Fast)
![진단모델](https://github.com/user-attachments/assets/573e8b0d-c24f-4c26-91c3-c5d7707612d0)
  - 위 모델은 YOLOv5 기반으로 하며, YOLO 계열 모델 중에서도 특히 속도와 정확도 균형이 좋아 실시간 애플리케이션에 많이 사용 됨
  - 특히 빠른 추론속도를 제공하도록 구성되어 있음
  - 또한 COCO 데이터셋을 기반으로 사전 학습된 모델임. -> COCO란 객체 감지, 분할, 키포인트 검출 등을 위해 널리 사용되는 대규모 데이터셋
  - COCO 데이터셋으로 사전 학습되어 있어 다양한 객체에 대한 기본적인 인식 능력을 갖추고 있음.
  - 데이터셋으로 추가 훈련(fine-tuning)을 할 때 빠르고 정확하며, 객체 감지 모델을 더 빠르게 최적화하고 성능을 높일 수 있음
<br/>

### 2. 데이터셋 : Kaggle 딸기 병해 객채 검출 데이터
  - 총 4301 병해 이미지
  - 종류 : 각진반점, 탄저병, 꽃곰팡이병, 잿빛곰팡이병, 세균모무늬병, 흰가루병(잎), 흰가루병(과일)
![데이터셋](https://github.com/user-attachments/assets/aa3678f2-fea2-4107-ac67-2e6765a7b74e)
<br/>

### 3. Training Graphs
  - mAP : 평균 정밀도라 하며 0과 1 사이에서 측정되고 1에 가까울 수록 더 정확한 모델임을 의미
![정확도](https://github.com/user-attachments/assets/447ada5f-8b7a-40d4-961d-57e4138b08a8)

![mAP](https://github.com/user-attachments/assets/8dd78722-7fd1-443f-af5b-39dd1414149b)

  - 검증세트(훈련 중 모델의 성능을 모니터링하고 최적화하는 데 사용)
![검증세트](https://github.com/user-attachments/assets/22a14551-b7a5-4cf9-85c9-0560e8ef28ee)

  - 테스트세트(최종적으로 모델의 성능을 평가하는 데 사용)
![테스트세트](https://github.com/user-attachments/assets/23dc7ac2-c139-47fb-ae02-300ff27f105b)
<br/>

### 4. 결과
  - 최종적으로 아래의 결과가 나옴
  - x축, y축, 너비, 높이, 신뢰도, 병명 등

![로보플로우 결과](https://github.com/user-attachments/assets/c1b12738-af86-4827-8c86-c41c513134c3)
<br/>

### 5. 테스트 영상
https://github.com/sojaeheon/smartfarm/assets/132196804/67dfe97b-c4b1-4a8c-8216-7248a1e67bcf
<br/>

### 6. 최종 결과
  - 다음 챗봇에서 나올 RAG와 접목하여 병해 솔루션 제공
![병해진단](https://github.com/user-attachments/assets/b22a5af1-7353-4e06-bcd7-904c4f61e3b4)
<br/><br/>

# 챗봇
## Google Gemini 사용
### 1. LLM 모델 : gemini-1.5-pro-001
![gemini](https://github.com/user-attachments/assets/a06d925f-2d42-410e-92ec-68d87ec26cd9)
<br/>

## RAG 검색 증강 생성
### 1. RAG란?
  - 대규모 언어 모델의 출력을 최적화하여 응답을 생성하기 전에 학습 데이터 소스 외부의 신뢰할 수 있는 지식 베이스를 참조하도록 하는 프로세스
<br/>

### 2. LangChain
  - 랭체인이란 개발자가 언어 모델을 기반으로 한 애플리케이션 개발 작업을 수월하게 진행할 수 있도록 설계된 오픈 소스 프레임워크
  - 한마디로 프롬포트, AI모델, 모델 답변 텍스트 도출을 하나의 연속적인 과정으로 만드는 것을 말함
![랭체인 흐름](https://github.com/user-attachments/assets/988bae61-fba3-4e6e-9115-26192e8865a9)
  - 흐름 예시
    #### 1. 데이터 소스 : LLM이 해당 작업을 수행하는 데 필요한 정보 (pdf, csv 등 외부 소스 데이터)
      - 농업 딸기 매뉴얼 pdf 사용
    #### 2. 단어 임베딩 : 데이터 소스를 벡터로 변환
      - pytorch기반의 HuggingFace 다국어 임베딩 모델 BAAI/bge-m3을 사용
    #### 3. 벡터 데이터베이스 : 생성된 임베딩을 유사성 검색을 위해 벡터 데이터베이스에 저장
      - ChromaDB 사용
    #### 4. 대규모 언어 모델(LLM) : 검색된 데이터를 기반으로 의미 있는 정보를 생성하는 데 필수적인 역할
      - gemini-1.5-pro-001 모델 사용
<br/>

### 3. 결과
![RAG1](https://github.com/user-attachments/assets/24702f7e-7517-48d3-b8bf-2bf1c0f7e8de)
![RAG2](https://github.com/user-attachments/assets/2cfab811-a350-42ee-88e0-f2ca8c9061bd)
<br/>

  - 화면 우측 상단에서 이전 대화 내용들을 확인 가능
![image](https://github.com/user-attachments/assets/3d63ed50-6b62-43ab-b758-61fbcc377fbc)





<hr>

# 시연 영상


[https://github.com/user-attachments/assets/35c1bfdc-3fda-47c9-9689-612d25f53005](https://github.com/user-attachments/assets/fcf754c1-b8f9-44ca-aba5-d2a6ca876fcf)


<br/>

# 기술 스택
![image](https://github.com/user-attachments/assets/d303936f-0600-4280-b0dc-3302de691349)
<br/>

# 일정(간트차트)
![image](https://github.com/user-attachments/assets/30d6a1e8-1827-4669-bd0a-5c428edcbf68)

