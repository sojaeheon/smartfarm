<template>
    <header>
        <div>
            <AppHeader />
        </div>
    </header>
    <div class="PhotoSelection" :class="{ 'menu-open': isMenuOpen }">
        <button class="Selection" @click="ShowModal = true">사진 선택..</button>
    </div>

    <!-- 사진 미리보기 -->
    <div class="photo-gallery">
      <img v-for="(photo, index) in photos" :key="index" :src="photo" @click="openDiagnosis(photo)" class="preview-image"/>
    </div>

    <!-- 모달 창: 카메라 또는 파일 선택 -->
    <div class="modal-background" v-if="ShowModal">
        <ul class="modal">
            <button class="close-button" @click="closeModal"></button>
            <li @click="openCamera">카메라</li>
            <li @click="openFilePicker">파일 선택</li>
        </ul>
    </div>

    <!-- 파일 선택 숨김 -->
    <input ref="fileInput" type="file" accept="image/*" @change="onFileChange" style="display: none;" />

    <!-- 진단 결과 모달 -->
    <div v-if="showDiagnosis" class="modal-background">
      <div class="modal">
        <button class="close-button" @click="closeDiagnosis"></button>
        <h3>진단 결과</h3>
        <p>병명: {{ diagnosis.disease }}</p>
        <p>솔루션: {{ diagnosis.solution }}</p>
      </div>
    </div>

</template>

<script>
import axios from 'axios';
import AppHeader from './AppHeader.vue';

export default {
    data() {
        return{
            ShowModal: false,
            photos: [], // 업로드된 사진을 저장하는 배열
            showDiagnosis: false, // 진단 결과 모달창 상태
            diagnosis: {
              disease: '',  //진단 결과의 병명
              solution: ''  //진단 결과의 솔루션
            },

            isMenuOpen: false,
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
                    this.photos.push(imageUrl);  // 배열에 추가하여 이미지 저장
                }
            }
        },
        async openDiagnosis(photo) {  
            try {
                // 파일을 FormData로 변환
                const formData = new FormData();
                formData.append('photo', photo.file);

                // 서버에 진단 요청 보내기
                const response = await axios.post('/api/diagnosis', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                });

                // 서버에서 받은 진단 결과 처리
                this.diagnosis.disease = response.data.disease;
                this.diagnosis.solution = response.data.solution;
                this.showDiagnosis = true;  // 모달 열기

            } catch (error) {
                console.error('진단 중 오류 발생:', error);
                alert('진단 중 오류가 발생했습니다.');
            }
        },
        closeDiagnosis() {
            this.showDiagnosis = false;
        },
        closeModal() {
            this.ShowModal = false;
        },
        toggleMenu() {
            this.isMenuOpen = !this.isMenuOpen;
        },
    },
}

</script>

<style>
.PhotoSelection {
    display: flex;
    top: 10px;
    left: 20px;
    width: 37vw;
    height: 20%;
    transform: transform 0.1s ease; /* 이동할 때 부드럽게 */
}
.Selection {
    background-color: #f0f0f0;
    border-radius: 10px;
    font-size: 20px;
    width: 25%;
    height: 45%;
    cursor: pointer;
    margin-top: 15px;
    margin-left: 20px;
    padding: 8px;
}

/* 모달 스타일 */
.modal-background {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5); /* 배경 어둡게 */
    display: flex;
    justify-content: center;
    align-items: center; /* 중앙 정렬 */
}

.modal {
    position: relative;
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    width: 80%;
    max-width: 300px;
    text-align: center;
    cursor: pointer;
}

.close-button {
    background-image: url('@/assets/closebutton.svg');
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    width: 30px;
    height: 30px;
    border: none;
    cursor: pointer;
    position: absolute;  /* 절대 위치로 설정 */
    top: 8px;  /* 모달의 상단에 붙이기 */
    right: 8px;  /* 모달의 오른쪽에 붙이기 */
}


/* li 태그 스타일 (버튼처럼 보이게) */
.modal li {
  list-style: none; /* 기본 리스트 스타일 제거 */
  padding: 10px 0; /* 항목마다 여백 추가 */
  border-bottom: 1px solid #ddd; /* 항목 구분선 */
  cursor: pointer;
  font-size: 1.25rem; /* 글자 크기 증가 */
} 

/* 마지막 항목은 구분선을 제거 */
.modal li:last-child {
  border-bottom: none;
}

.photo-gallery {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); /* 이미지가 화면에 맞게 정렬되도록 */
    gap: 8px; /* 이미지 간의 간격을 설정 */
    margin-top: 20px; /* 상단 여백 */
    max-height: calc(100vh - 200px); /* 화면 높이에서 메뉴바 높이를 뺀 크기를 지정 */
    overflow-y: auto; /* 세로로 스크롤이 생기도록 설정 */
    padding-right: 10px; /* 스크롤바로 인한 오른쪽 여백 */
}

/* 이미지 미리보기 스타일 */
.preview-image {
    width: 150px;
    height: 200px; /* 이미지의 가로세로 비율을 유지하면서 자동으로 크기 조절 */
    object-fit: contain; 
    border-radius: 5px;
    cursor: pointer;
    margin-top: 10px;
    margin-left: 20px;
}
/* 모바일 화면에서 버튼 크기와 여백 조정 */
@media (max-aspect-ratio: 1/1) {
    .Selection {
        width: 50%;
        height: 30%;
    }
    .modal {
        width: 90%;
    }
}

</style>