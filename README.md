# 조명은 LED - Smartfarm

## 조원
* 하승철
* 박현준
* 소재헌
* 최유정
* 하령경

## 노션
조명은 LED - (https://www.notion.so/daa597b71e6b46b9a22b0299711b95e0)

# 블록도
![시스템 구조](https://github.com/user-attachments/assets/4b9d4742-b575-406a-a66b-e95716be5bf6)
<br/>

# 흐름도
![작품 흐름도](https://github.com/user-attachments/assets/011de612-fadf-451e-86e5-361ed4fed86f)
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
<br/>

# 로그인
<br/><br/>

# 메인
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
<br/><br/>

# 챗봇
## Google Gemini 이용
### 1. LLM 모델 : gemini-1.5-pro-001
![gemini](https://github.com/user-attachments/assets/ecbfd7c3-e5c0-40ab-ae94-98d157fa9f77)
<br/>

## RAG 검색 증강 생성
### 1. RAG란?
  - 대규모 언어 모델의 출력을 최적화하여 응답을 생성하기 전에 학습 데이터 소스 외부의 신뢰할 수 있는 지식 베이스를 참조하도록 하는 프로세스
<br/>

### 2. LangChain
  - 랭체인이란 개발자가 언어 모델을 기반으로 한 애플리케이션 개발 작업을 수월하게 진행할 수 있도록 설계된 오픈 소스 프레임워크
  - 한마디로 프롬포트, AI모델, 모델 답변 텍스트 도출을 하나의 연속적인 과정으로 만드는 것을 말함
![랭체인 흐름](https://github.com/user-attachments/assets/988bae61-fba3-4e6e-9115-26192e8865a9)



<hr>

# Block #1 
* window 환경에서 진행
* Python을 이용하여 대화형 웹 애플리케이션을 쉽게 구현 할 수 있는 웹 프레임워크 Streamlit 사용
  ![image](https://github.com/sojaeheon/smartfarm/assets/144245586/b948724d-7db3-4fa1-9a9f-f4b5a06704b5)
  
* 병해 이미지 업로드
   - 업로드를 하게 되면 roboflow 모델 호출
  ![image](https://github.com/sojaeheon/smartfarm/assets/144245586/a411f024-8ad9-4402-912d-af4670d1e503)

# Block #2
* roboflow 사용
1. 모델 : Roboflow 3.0
2. traing 그래프
   
![image](https://github.com/sojaeheon/smartfarm/assets/132196804/cc9580ed-6838-4876-aabf-fdb4f9ce63f1)

4. 데이터 셋
+ Kaggle : 딸기 병해 객채 검출 데이터
+ 총 4301 병해 이미지
+ 종류 : 각진반점, 탄저병, 꽃곰팡이병, 잿빛곰팡이병, 세균모무늬병, 흰가루병(잎), 흰가루병(과일)

![image](https://github.com/sojaeheon/smartfarm/assets/119103469/41a0e586-e9b7-4d3b-ae74-360f9b4de652)


5. 테스트 영상
https://github.com/sojaeheon/smartfarm/assets/132196804/67dfe97b-c4b1-4a8c-8216-7248a1e67bcf

# Block #3
* AI의 답변
1. 위의 모델로 얻은 결과를 프롬포트로 만들어 AI모델을 호출
   * SIONIC AI사의 xionic-ko-llama-3-70b이라는 한국어 모델을 사용-(https://github.com/sionic-ai/xionic-ko-llama-3-70b)
   ![image](https://github.com/sojaeheon/smartfarm/assets/144245586/b6645dc4-f96d-46b8-8856-cc328fca33e9)
2. 체인 생성
   * 프롬포트, AI모델, 모델 답변 텍스트 도출을 체인
   * 여기서 체인이란 일련의 작업 단계를 하나의 연속적인 과정을 만드는 것을 말함
3. AI의 답변
![image](https://github.com/sojaeheon/smartfarm/assets/144245586/600552a6-3324-47d4-bc74-f294ff175586)

<br/><br/>
<hr>
<br/><br/>

# 블록도
![image](https://github.com/user-attachments/assets/b515da2e-6144-43fd-8766-6d53eaaef35b)
<hr>
![image](https://github.com/user-attachments/assets/e376084a-bb6c-4c1d-ba26-a5efa567a354)



# 일정(간트차트)
![image](https://github.com/user-attachments/assets/30d6a1e8-1827-4669-bd0a-5c428edcbf68)


# 주요 기능
### 1. 로그인
#### 1.1 사용자 로그인

### 2. 메인
#### 2.1 실시간 환경 센서값
#### 2.2 엑츄에이터 작동
#### 2.3 일기예보 API

### 3. 병해진단페이지
#### 3.1 사진을 넣거나 찍어서 병해 확인

### 4. 챗봇페이지
#### 4.1 질문에 대한 답변을 얻을 수 있음

### 5. 스마트팜 환경그래프 페이지 
#### 5.1 스마트팜 내 환경을 그래프로 확인 

## 영상
https://github.com/user-attachments/assets/60d6e221-28a6-4da9-ba84-22db664abf0f

  
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
# 방향

## 1. RAG
* 검생 증강 생성(RAG)을 통해 보다 더 정확한 솔루션 제공
* 딸기 매뉴얼을 토대로한 AI의 답변
   * pytorch기반의 HuggingFace 다국어 임베딩 모델 BAAI/bge-m3을 사용 
![image](https://github.com/sojaeheon/smartfarm/assets/144245586/96d31ba2-50d7-4d5e-bb12-3fa55727434f)
![image](https://github.com/sojaeheon/smartfarm/assets/144245586/71bf9aa9-08ab-4567-a0c9-643830bec7c9)

