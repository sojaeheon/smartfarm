<template>
    <header>
        <div>
            <AppHeader />
        </div>
    </header>
    <div class="PhotoSelection">
        <button class="Selection" @click="ShowModal = true">사진 선택..</button>
    </div>

    <!-- 사진 미리보기 -->
    <div class="photo-gallery">
      <img v-for="(photo, index) in photos" :key="index" :src="photo" @click="openDiagnosis(photo)" class="preview-image"/>
    </div>

    <!-- 모달 창: 카메라 또는 파일 선택 -->
    <div v-if="showModal" class="modal-background">
      <div class="modal">
        <button class="close-button" @click="closeModal">X</button>
        <button @click="openCamera">카메라</button>
        <button @click="openFilePicker">파일 선택</button>
      </div>
    </div>

    <!-- <div class="modal" v-if="ShowModal == true">
        <ui class="modal-content">
            <li @click="openCamera">카메라</li>
            <li @click="openFilePicker">파일 선택</li>
            <li @click="ShowModal = false">닫기</li>
        </ui>
    </div> -->
    <!-- 파일 선택 숨김 -->
    <input ref="fileInput" type="file" accept="image/*" @change="onFileChange" style="display: none;" />

    <!-- 업로드된 이미지 리스트 -->
    <!-- <div class="uploaded-images">
        <div v-for="(imageUrl, index) in imageUrls" :key="index" class="image-wrapper">
            <img :src="imageUrl" alt="업로드된 이미지" class="uploaded-image" />
        </div>
    </div> -->

    <!-- 진단 결과 모달 -->
    <div v-if="showDiagnosis" class="modal-background">
      <div class="modal">
        <button class="close-button" @click="closeDiagnosis"></button>
        <h3>병해진단 결과</h3>
        <p>{{ diagnosis }}</p>
      </div>
    </div>
</template>

<script>
import AppHeader from './AppHeader.vue';

export default {
    data() {
        return{
            photos: [], // 업로드된 사진을 저장하는 배열
            showModal: false, // 사진 선택 모달창 상태
            showDiagnosis: false, // 진단 결과 모달창 상태
            diagnosis: '', // 진단 결과 저장

            // ShowModal: false,
            // imageUrls: [],     // 업로드된 이미지들의 URL을 저장하는 배열
        }
    },
    components: {
        AppHeader
    },
    methods: {
        // 카메라를 열기 위한 메서드 (모바일 카메라를 사용 가능)
        openCamera() {
            this.$refs.fileInput.setAttribute('capture', 'camera'); // 카메라로 사진 촬영
            this.$refs.fileInput.click();
            this.ShowModal = false;  // 모달 닫기
        },
        // 파일 선택을 위한 메서드
        openFilePicker() {
            this.$refs.fileInput.removeAttribute('capture'); // 파일 선택
            this.$refs.fileInput.click();
            this.ShowModal = false;  // 모달 닫기
        },
        // 파일 선택 후 이미지 미리보기
        onFileChange(event) {
            const files = event.target.files;
            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                if (file) {
                    const imageUrl = URL.createObjectURL(file);  // 이미지 URL 생성
                    this.imageUrls.push(imageUrl);  // 배열에 추가하여 이미지 저장
                }
            }
        },
        openDiagnosis(photo) {  // 진단 내용을 불러오고 모달을 엽니다.
            this.diagnosis = `진단 결과: ${photo}`;
            this.showDiagnosis = true;
        },
        closeDiagnosis() {
            this.showDiagnosis = false;
        },
    },
}

</script>

<style>
.PhotoSelection {
    display: flex;
    height: 40vh;
    margin-top: 15px;
    margin-left: 30px;
}
.Selection {
    background-color: #f0f0f0;
    border-radius: 10px;
    font-size: 20px;
    width: 20%;
    height: 40%;
    cursor: pointer;
}

/* 모달 스타일 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 40%; /* 전체 너비 */
  height: 40%; /* 전체 높이 */
  background-color: rgba(0, 0, 0, 0.5); /* 반투명 검정 배경 */
  display: flex;
  justify-content: center;
  align-items: center; /* 가운데 정렬 */
}

.modal-content {
  background-color: white;
  padding: 15px;
  border-radius: 10px;
  width: 100%; /* 화면 크기에 맞게 조정 */
  max-width: 400px; /* 최대 크기 설정 */
  box-sizing: border-box; /* 패딩과 테두리를 포함한 크기 계산 */
  text-align: center;
}

/* li 태그 스타일 (버튼처럼 보이게) */
.modal-content li {
  list-style: none; /* 기본 리스트 스타일 제거 */
  padding: 10px 0; /* 항목마다 여백 추가 */
  border-bottom: 1px solid #ddd; /* 항목 구분선 */
  cursor: pointer;
  font-size: 1.25rem; /* 글자 크기 증가 */
}

/* 마지막 항목은 구분선을 제거 */
.modal-content li:last-child {
  border-bottom: none;
}

.close-button {
    background-image: url(../assets/);
}

/* 모달 스타일
.modal {
    position: fixed;
    top: 0;
    width: 40%;
    height: 40%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center; */
    /* align-items: center; */
    /* border-radius: 10px; */
    /* max-width: 400px; 최대 크기 설정 */
/* }
.modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    text-align: center; */
    /* width: 100%; 화면 크기에 맞게 조정 */
    /* max-width: 400px; 최대 크기 설정 */
    /* box-sizing: border-box; 패딩과 테두리를 포함한 크기 계산 */
    
    /* cursor: pointer;
} */

.preview {
    margin-top: 20px;
    text-align: center;
}

.preview-image {
    max-width: 100%;
    height: auto;
    border-radius: 10px;
}


/* 모바일 화면에서 버튼 크기와 여백 조정 */
@media (max-width: 768px) {
    .modal-content button {
        font-size: 0.9rem; /* 모바일에서 버튼 텍스트 크기 조정 */
        padding: 8px 16px; /* 모바일에서 버튼 패딩 조정 */
    }
}
</style>