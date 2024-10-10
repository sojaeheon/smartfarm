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
![image](https://github.com/sojaeheon/smartfarm/assets/144245586/cfb397f3-ccad-418b-a793-76ab83f630d1)

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
![image](https://github.com/user-attachments/assets/fd68ece7-91a3-488e-8267-ff20a9ef9453)
# 병해 진단
![image](https://github.com/user-attachments/assets/39fdf106-4f69-4456-922f-8fc70a632726)
# AI 챗봇
![image](https://github.com/user-attachments/assets/cd64ab9e-5301-4530-8242-2d314b53e52f)


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

#영상
https://github.com/user-attachments/assets/60d6e221-28a6-4da9-ba84-22db664abf0f

  
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
# 방향

## 1. RAG
* 검생 증강 생성(RAG)을 통해 보다 더 정확한 솔루션 제공
* 딸기 매뉴얼을 토대로한 AI의 답변
   * pytorch기반의 HuggingFace 다국어 임베딩 모델 BAAI/bge-m3을 사용 
![image](https://github.com/sojaeheon/smartfarm/assets/144245586/96d31ba2-50d7-4d5e-bb12-3fa55727434f)
![image](https://github.com/sojaeheon/smartfarm/assets/144245586/71bf9aa9-08ab-4567-a0c9-643830bec7c9)

## 2. stt - tts
* Python 라이브러리 gTTS를 이용해 음성으로 대화


## 3. 스마트팜 환경제어
* 블록도
  
![image](https://github.com/sojaeheon/smartfarm/assets/132196804/798ce32d-b311-41f1-b988-9a10f7976752)



