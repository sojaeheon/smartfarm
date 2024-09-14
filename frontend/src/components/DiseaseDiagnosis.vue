<template>
    <header>
        <div>
            <AppHeader />
        </div>
    </header>
    <div class="PhotoSelection">
        <button class="Selection" @click="ShowModal = true">사진 선택..</button>
    </div>
    <!-- 모달 창: 카메라 또는 파일 선택 -->
    <div v-if="ShowModal" class="modal">
        <ui class="modal-content">
            <li @click="openCamera">카메라</li>
            <li @click="openFilePicker">파일 선택</li>
            <li @click="ShowModal = false">닫기</li>
        </ui>
    </div>
    <!-- 파일 선택 숨김 -->
    <input ref="fileInput" type="file" accept="image/*" @change="onFileChange" style="display: none;" />

    <!-- 업로드된 이미지 리스트 -->
    <div class="uploaded-images">
        <div v-for="(imageUrl, index) in imageUrls" :key="index" class="image-wrapper">
            <img :src="imageUrl" alt="업로드된 이미지" class="uploaded-image" />
        </div>
    </div>
</template>

<script>
import AppHeader from './AppHeader.vue';

export default {
    data() {
        return{
            ShowModal: false,
            imageUrls: [],     // 업로드된 이미지들의 URL을 저장하는 배열
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
    width: 40%;
    height: 40%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    /* align-items: center; */
    border-radius: 10px;
    max-width: 400px; /* 최대 크기 설정 */
}
.modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    width: 100%; /* 화면 크기에 맞게 조정 */
    max-width: 400px; /* 최대 크기 설정 */
    box-sizing: border-box; /* 패딩과 테두리를 포함한 크기 계산 */
    
    cursor: pointer;
}

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