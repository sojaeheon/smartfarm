<template>
  <header>
    <div>
      <AppHeader />
    </div>
  </header>
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
import AppChatbotModal from './AppChatbotModal.vue';
import AppHeader from './AppHeader.vue';

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
    AppHeader,
    AppChatbotModal,
  },
  updated() {
    // 컴포넌트 업데이트 후 스크롤을 맨 아래로 자동 조정
    this.scrollToBottom();
  }
};
</script>

<style>
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
  flex-direction: column;
  /* 위아래 배치 */
  height: 85vh;
  width: 85vw;
  margin: 1vw 0 0 2vw;
  /* margin: 2vw 0 10px 10vw; */
  position: relative;
  background-color: rgba(99, 199, 88, 0.3);
  border-radius: 8px;
  padding: 10px;
  justify-content: flex-end;
  /* 메시지들을 아래쪽으로 정렬 */
}

#search-list {
  position: fixed;
  top: 17px;
  right: 20px;
  background-image: url('../assets/inbox.svg');
}

.messages {
  display: flex;
  flex-direction: column;
  /* 메시지를 위에서 아래로 쌓이게 함 */
  gap: 10px;
  /* 메시지들 사이의 간격 */
  max-height: 70vh;
  /* 최대 높이 설정 */
  flex-grow: 1;
  /* 가능한 공간을 모두 차지하도록 설정 */
  margin-bottom: 10px;
  /* 입력창 바로 위로 붙이기 위한 마진 */
  margin-top: auto;
  overflow-y: auto;
  /* 스크롤 가능하도록 설정 */
}

.messages> :first-child {
  margin-top: auto;
}

.message {
  display: flex;

  justify-content: flex-end; /* 사용자 메시지를 오른쪽으로 정렬 */
  color: rgba(0, 0, 0, 0.7);
}

.message.ai {
  justify-content: flex-start; /* AI 메시지는 왼쪽으로 정렬 */
  color: white;
}

.message-text {
  padding: 10px;
  border-radius: 10px;
  max-width: 60%;
  background-color: rgba(250, 120, 45, 0.5);
  z-index: 1;
}

/* 사용자 메시지 스타일 추가 */
.message.user .message-text {
  background-color: rgba(250, 120, 45, 0.5); /* 사용자 메시지 배경색 */
}

.input-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 10px;
}

.chat-bot input {
  height: 5vh;
  width: 85vw;
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
