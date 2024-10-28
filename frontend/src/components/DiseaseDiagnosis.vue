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
        <img v-for="(photo, index) in photos" :key="index" :src="photo.url" @click="openDiagnosis(photo)"
            class="preview-image" />
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
    <div v-if="showDiagnosis" class="modal-background-Diagnosis">
        <div class="modal-Diagnosis">
            <button class="close-button" @click="closeDiagnosis"></button><br>
            <h2>진단 결과</h2>
            <div class="modal-p">
                <!-- <img :src="selectedPhoto" class="diagnosis-image" alt="진단 결과 이미지" /> -->
                <img :src="'data:image/png;base64,' + diagnosis.boundingImage" class="diagnosis-image" alt="진단 결과 이미지" />
                <p><b>병명:</b> {{ diagnosis.disease }}</p>
                <p><b>해결책:</b> <span v-html="diagnosis.solution"></span></p>
            </div>
        </div>
    </div>

    <!-- 로딩 화면 -->
    <div v-if="isLoading" class="loading-overlay">
        <p>병해진단 중입니다... 잠시만 기다려 주세요.</p>
    </div>
</template>

<script>
import axios from 'axios';
import AppHeader from './AppHeader.vue';

export default {
    data() {
        return {
            ShowModal: false,
            photos: [], // 업로드된 사진을 저장하는 배열
            showDiagnosis: false, // 진단 결과 모달창 상태
            isLoading: false, // 로딩 상태
            diagnosis: {
                disease: '',     //진단 결과 병명
                solution: '',    //진단 결과 솔루션
                resultImage: '', //진단 결과 이미지
            },
            isMenuOpen: false,

            //selectedPhoto: '', // 선택된 업로드 사진(test)
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
                    this.photos.push({
                        url: imageUrl,  // 미리보기 이미지 URL
                        file: file      // 실제 파일 객체
                    });
                }
            }
        },
        // test용
        // openDiagnosis(photo) {
        //     this.selectedPhoto = photo;
        //     try {
        //         this.diagnosis.disease = "곰팡이";
        //         this.diagnosis.solution = "ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ";
        //         this.showDiagnosis = true;  // 모달 열기
        //     } catch (error) {
        //         console.error('진단 중 오류 발생:', error);
        //         alert('진단 중 오류가 발생했습니다.');
        //     }
        // },

        // 병해진단 수행
        async openDiagnosis(photo) {
            try {
                this.isLoading = true;                 // 로딩 화면 표시
                const formData = new FormData();       // 파일을 FormData로 변환
                formData.append('photo', photo.file);  // 파일 객체 전송

                // http://192.168.0.29:8888/api/disease
                // http://192.168.25.5:8888/api/disease
                // 서버에 진단 요청 보내기
                const response = await axios.post('/api/ai/disease', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                });
                // 서버에서 받은 진단 결과 처리
                this.diagnosis.disease = response.data.disease;
                this.diagnosis.solution = response.data.solution.replace(/\n/g, '<br>');
                this.diagnosis.boundingImage = response.data.boundingImage;
                this.showDiagnosis = true;  // 모달 열기
            } catch (error) {
                console.error('진단 중 오류 발생:', error);
                alert('진단 중 오류가 발생했습니다.');
            } finally {
                this.isLoading = false;  // 로딩 화면 숨기기
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
    transform: transform 0.1s ease;
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
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
}

.modal-background-Diagnosis {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
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

.modal-Diagnosis {
    position: relative;
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    width: 90%;
    max-width: 380px;
    text-align: center;
    cursor: pointer;
}

.modal-Diagnosis h2 {
    color: #FA782D;
    padding-bottom: 10px;
    border-bottom: 1px solid #ddd;
}

.modal-Diagnosis p {
    margin-top: 7px;
}

.modal-p {
    margin: 10px;
    max-height: 300px;
    overflow-y: auto;
    padding-right: 10px;
    box-sizing: border-box;
}

.modal-p::-webkit-scrollbar {
    width: 8px;
}

.modal-p::-webkit-scrollbar-thumb {
    background-color: #FA782D;
    border-radius: 10px;
}

.modal-p::-webkit-scrollbar-track {
    background-color: #f1f1f1;
    border-radius: 10px;
}

.diagnosis-image {
    width: 90%;
    /* 가로 */
    height: 208px;
    /* 세로 */
    object-fit: contain;
    margin-right: 10px;
    border-radius: 5px;
}

.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 18px;
    z-index: 9999;
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
    position: absolute;
    top: 8px;
    right: 8px;
}

/* li 태그 스타일 (버튼처럼 보이게) */
.modal li {
    list-style: none;
    padding: 10px 0;
    border-bottom: 1px solid #ddd;
    cursor: pointer;
    font-size: 1.25rem;
}

/* 마지막 항목은 구분선을 제거 */
.modal li:last-child {
    border-bottom: none;
}

.photo-gallery {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 8px;
    margin-top: 20px;
    max-height: calc(100vh - 200px);
    overflow-y: auto;
    padding-right: 10px;
}

/* 이미지 미리보기 스타일 */
.preview-image {
    width: 150px;
    height: 200px;
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