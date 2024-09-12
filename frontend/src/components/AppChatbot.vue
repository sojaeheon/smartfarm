<template>
  <div>
    <MenuList /> 
  </div>
  <main class="main">
    <div class="chat-bot">
      <div>
        <button id="search-list"></button>
      </div>
      <div class="messages">
        <div v-for="message in messages" :key="message.id" class="message">
          <div :class="`message-${message.sender}`">{{ message.text }}</div>
        </div>
      </div>
      <div class="input-container">
        <input v-model="userInput" @keyup.enter="sendMessage" placeholder="메시지 입력..." />
        <button type="submit" @click="sendMessage"></button>
      </div>
    </div>
  </main>
</template>
  
<script>
import axios from 'axios';
import MenuList from '../components/MenuList.vue';
  
export default {
  data() {
    return {
      userInput: '',
      messages: []
    };
  },
  methods: {
    async sendMessage() {
      const userMessage = this.userInput.trim();
      if (!userMessage) return;
  
      this.addMessage('user', userMessage);
  
      const aiResponse = await this.getAIResponse(userMessage);
      this.addMessage('ai', aiResponse);
  
      this.userInput = '';
    },
    addMessage(sender, text) {
      this.messages.push({ id: Date.now(), sender, text });
    },
    async getAIResponse(message) {
      try {
        const response = await axios.post('AI_API_ENDPOINT', {
          prompt: message,
          // 다른 필요한 API 매개변수
        }, {
          headers: {
            'Authorization': `Bearer YOUR_API_KEY`
          }
        });
  
        return response.data.choices[0].text.trim();
      } catch (error) {
        console.error('AI 응답 오류:', error);
        return '죄송합니다, 오류가 발생했습니다.';
      }
    }
  },
  components: {
    MenuList
  }
};
</script>
  
<style>
/* 여기에 챗봇 스타일 추가 */
.main {
  display: inline-block;
  display: flex;
  justify-content: center; /* 가로축 중앙 정렬 */
  align-items: center; /* 세로축 중앙 정렬 */
  height: 100vh; /* 화면 전체 높이를 차지하도록 설정 */
  background-color: snow;
}
.chat-bot {
  margin: 10px 0; /*위 아래 여백*/
  position: absolute;
  justify-content: center;
  bottom: 5vh;
  border: 2px solid blue;
}
#search-list {
  position: fixed;
  top: 5px;
  right: 20px;
  background-image: url('../assets/settings.svg'); /*검색기록 이미지 찾기*/
}
.chat-bot input{
  height: 5vh;
  width: 60vw;
  padding: 0px 20px 0px 20px;
  font-size: 1rem;
  border-radius: 30px;
  border: 2px solid #F99E17;
}
.chat-bot button {
  position: absolute;
  right: 2vw;
  top: 5px;
  background-image: url('../assets/search.svg');
}
</style>
  