<template>
  <header>
        <button id="menu-button" v-if="isMobile" @click="toggleShow"></button>
        <img src="../assets/Farmi.svg" alt="farmi" height="50vh">
    
        <div class="menuWrap">
            <ul class="loginclick">
                <li><router-link to="/LoginView">로그인</router-link></li>
            </ul>
        </div>
    </header>
    <div>
      <MenuList />
    </div>
    <section class="main">
      <div class="chat-bot">
        <div>
          <button id="search-list" @click="showSearchList"></button>
          <div v-if="isListOpen" class="modal-overlay" @click="closeModal">
            <AppChatbotModal :lists="lists" @closeModal="closeModal" />
          </div>
        </div>
        <div class="messages" ref="messages">
        <div v-for="message in messages" :key="message.id" class="message" :class="message.sender">
          <div class="message-text">{{ message.text }}</div>
        </div>
      </div>
      <div class="input-container">
        <input v-model="userInput" @keyup.enter="sendMessage" placeholder="메시지 입력..." />
        <button type="submit" @click="sendMessage"></button>
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios';
import MenuList from './MenuList.vue';
import AppChatbotModal from './AppChatbotModal.vue';

export default {
  data() {
    return {
      isListOpen: false, // 모달의 상태
      lists: ['이거', '저거', '요거'],
      userInput: '',
      messages: []
    };
  },
  methods: {
    showSearchList() {
      this.isListOpen = true; // 모달 열기
    },
    closeModal() {
      this.isListOpen = false; // 모달 닫기
    },
    async sendMessage() {
      const userMessage = this.userInput.trim();
      if (!userMessage) return;

      this.addMessage('user', userMessage);

      const aiResponse = await this.getAIResponse(userMessage);
      this.addMessage('ai', aiResponse);

      this.userInput = '';
      this.scrollToBottom(); // 메시지 전송 후 스크롤 내리기
    },
    addMessage(sender, text) {
      this.messages.push({ id: Date.now(), sender, text });
    },
    async getAIResponse(message) {
      try {
        const response = await axios.post(
          'AI_API_ENDPOINT',
          {
            prompt: message
          },
          {
            headers: {
              Authorization: `Bearer YOUR_API_KEY`
            }
          }
        );

        return response.data.choices[0].text.trim();
      } catch (error) {
        console.error('AI 응답 오류:', error);
        return '죄송합니다, 오류가 발생했습니다.';
      }
    },
    scrollToBottom() {
    const messagesContainer = this.$refs.messages;
    if (messagesContainer) {
      messagesContainer.scrollTop = messagesContainer.scrollHeight; // 스크롤을 맨 아래로 내리기
    }
    }
  },
  components: {
    MenuList,
    AppChatbotModal,
  },
  updated() {
    // 컴포넌트 업데이트 후 스크롤을 맨 아래로 자동 조정
    this.scrollToBottom();
  }
};
</script>

<style>
header {
border-bottom: 2px solid black;
display: flex;
justify-content: space-between; /* 좌우로 아이템 배치 */
align-items: center; /* 세로로 가운데 정렬 */
padding: 12px;
position: fiexed;
}
button {
  width: 35px;
  height: 35px;
  background-color: white;
  background-size: cover;
  border: none;
}
.main {
  display: flex;
}
.chat-bot {
  display: flex;
  flex-direction: column; /* 위아래 배치 */
  height: 80vh;
  width: 60vw;
  margin: 10px 0 10px 10vw;
  position: relative;
  background-color: rgba(99, 199, 88, 0.3);
  border-radius: 10px;
  padding: 10px;
  justify-content: flex-end; /* 메시지들을 아래쪽으로 정렬 */
}
#search-list {
  position: fixed;
  top: 5px;
  right: 20px;
  background-image: url('../assets/settings.svg'); /* 검색기록 이미지 찾기 */
}
.messages {
  display: flex;
  flex-direction: column; /* 메시지를 위에서 아래로 쌓이게 함 */
  gap: 10px; /* 메시지들 사이의 간격 */
  max-height: 60vh; /* 최대 높이 설정 */
  flex-grow: 1; /* 가능한 공간을 모두 차지하도록 설정 */
  margin-bottom: 10px; /* 입력창 바로 위로 붙이기 위한 마진 */
  margin-top: auto;
  overflow-y: auto; /* 스크롤 가능하도록 설정 */
}
.messages > :first-child {
  margin-top: auto;
}
.message {
  display: flex;
}
.message-text {
  padding: 10px;
  border-radius: 10px;
  max-width: 60%;
  background-color: rgba(250,120,45,0.5);
  z-index: 1;
}
.input-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 10px;
}
.chat-bot input {
  height: 5vh;
  width: 60vw;
  padding: 0px 20px 0px 20px;
  font-size: 1rem;
  border-radius: 30px;
  border: 2px solid #F99E17;
  outline: none;
}
.chat-bot button {
  width: 4vh;
  height: 4vh;
  background-image: url('../assets/search.svg');
  border-radius: 50px;
}
</style>
