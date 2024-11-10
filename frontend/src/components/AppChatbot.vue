<template>
  <header>
    <div>
      <AppHeader />
    </div>
  </header>
  <section class="main">
    <div class="chat-bot">
      <div>
        <button id="search-list" @click="fetchSearchHistory"></button>
        <div v-if="isListOpen" class="modal-overlay" @click="closeModal">
          <AppChatbotModal :lists=lists @closeModal="closeModal" @deleteItem="deleteSearchHistoryItem"
            @selectSession="loadSessionData" />
        </div>
      </div>
      <div class="messages" ref="messages">
        <div v-for="message in messages" :key="message.id" class="message" :class="message.sender">
          <!-- <div class="message-text">{{ message.text }}</div> -->
          <div class="message-text" v-html="message.text"></div>
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
      lists: ["이거","저거","요거"],
      userInput: '',
      messages: [],
      chat_sessions: null,
    };
  },
  methods: {
    showSearchList() {
      this.isListOpen = true; // 모달 열기
    },
    async fetchSearchHistory() {
      try {
        const response = await axios.get('/api/chat_history',{
          params:{
            username : this.$store.state.userId
          }
        });

        this.lists = response.data.history; // 서버에서 받은 검색 기록 저장
        this.isListOpen = true; // 모달 열기
      } catch (error) {
        console.error('검색 기록을 불러오는 중 오류 발생:', error);
      }
    },
    closeModal() {
      this.isListOpen = false; // 모달 닫기
    },
    
    //세션 항목 제거하기
    async deleteSearchHistoryItem(index) {
      const item = this.lists[index];
      try {
        await axios.delete(`/api/delete_history/${item.session_id}`);
        this.lists.splice(index, 1); // 배열에서 해당 항목 제거
      } catch (error) {
        console.error('검색 기록 삭제 오류:', error);
      }
    }, 

    //해당 세션 대화 불러오기
    async loadSessionData(sessionId) {
      try {
        const response = await axios.get(`/api/session/${sessionId}`);
        const sessionData = response.data.history; // DB에서 반환된 question과 answer

        // 서버에서 불러온 데이터를 messages 배열로 변환
        this.messages = sessionData.map((item) => ({
          id: item.message_id,          // 메시지의 고유 ID
          sender: item.sender,          // 메시지의 발신자 ('user' 또는 'ai')
          text: item.message_text,      // 메시지 내용
          date: item.timestamp          // 메시지 전송 시간
        }));

        // 모달 닫기
        this.closeModal();
      } catch (error) {
        console.error('세션 데이터 불러오기 오류:', error);
      }
    },

    async sendMessage() {
      const userMessage = this.userInput.trim();
      if (!userMessage) return;
      this.userInput = '';
      this.addMessage('user', userMessage);

      
      if(this.chat_sessions === null){
        // 새로운 세션을 서버에 생성하는 API 호출
        try {
          const response = await axios.post('/api/session/new', {
            question: userMessage,
            username: this.$store.state.userId,
          });

          // 새로운 세션 정보 받아오기
          const newSession = response.data;

          this.chat_sessions = newSession.session_id;
          // 새로운 세션을 목록의 첫번째에 추가
          this.lists.unshift(newSession);
          
        } catch (error) {
          console.error('새로운 세션 생성 오류:', error);
        }
      }

      const aiResponse = await this.getAIResponse(userMessage);
      this.addMessage('ai', aiResponse);

      this.scrollToBottom(); // 메시지 전송 후 스크롤 내리기
    },
    async endSession() {
      if (this.chat_sessions !== null) {
        try {
          // 세션 종료 API 호출
          await axios.post(`/api/session/${this.chat_sessions}/end`);
          this.chat_sessions = null;  // 세션 ID 초기화
        } catch (error) {
          console.error('세션 종료 오류:', error);
        }
      }
    },
    addMessage(sender, text) {
      this.messages.push({ id: Date.now(), sender, text });
    },

    async getAIResponse(message) {
      try {
        const response = await axios.post('/api/ai/get_answer', {
          question: message,
          username: this.$store.state.userId,
          session_id: this.chat_sessions
          // 다른 필요한 API 매개변수
        }, {
          headers: {
            'Content-Type': `application/json`
          }
        });


        return response.data.answer.replace(/\n/g, '<br>');
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
  created() {
    // 초기 AI 메시지 추가
    this.addMessage('ai', '😀안녕하세요! 팜이입니다!😀');
  },
  updated() {
    // 컴포넌트 업데이트 후 스크롤을 맨 아래로 자동 조정
    this.scrollToBottom();
  },
  mounted() {
    // 창을 닫거나 페이지를 나갈 때 세션 종료 API 호출
    window.addEventListener('beforeunload', this.endSession);
  },
  beforeUnmount() { // Vue 3에서는 beforeUnmount 사용
    this.endSession();
    window.removeEventListener('beforeunload', this.endSession);
  },
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
  margin: 1vh 0 0 1vw;
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

  justify-content: flex-end;
  /* 사용자 메시지를 오른쪽으로 정렬 */
  color: black;
}

.message.ai {
  justify-content: flex-start;
  /* AI 메시지는 왼쪽으로 정렬 */
  color: black;
}

.message-text {
  padding: 10px;
  border-radius: 10px;
  max-width: 60%;
  background-color: rgba(250, 120, 45, 0.5);
  font-weight: 600;
  font-size: 1rem;
  z-index: 1;
}

/* 사용자 메시지 스타일 추가 */
.message.user .message-text {
  background-color: rgba(250, 120, 45, 0.5);
  /* 사용자 메시지 배경색 */
}

.input-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 10px;
}

.input-container input {
  height: 5vh;
  width: 85vw;
  padding: 0px 20px 0px 20px;
  font-size: 1rem;
  border-radius: 30px;
  border: 2px solid #F99E17;
  outline: none;
}

.input-container button {
  width: 4vh;
  height: 4vh;
  background-image: url('../assets/search.svg');
  border-radius: 15px;
  background-color: rgba(99, 199, 88, 0.1);
}

@media (max-aspect-ratio: 1/1) {
  .chat-bot {
    width: 93vw;
  }
}
</style>
