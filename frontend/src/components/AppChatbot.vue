<template>
  <div class="chat-bot">
      <div class="messages">
        <div v-for="message in messages" :key="message.id" class="message">
          <div :class="`message-${message.sender}`">{{ message.text }}</div>
        </div>
      </div>
    <input v-model="userInput" @keyup.enter="sendMessage" placeholder="메시지 입력..." />
    <button type="submit"></button>
  </div>
</template>
  
<script>
import axios from 'axios';
  
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
  }
};
</script>
  
<style>
/* 여기에 챗봇 스타일 추가 */
.chat-bot input{
  height: 5vh;
  width: 60vw;
  position: relative;
  padding: 0px 20px 0px 20px;
  font-size: 1rem;
  border-radius: 30px;
  border: 2px solid #F99E17;
}
.chat-bot button {
  position: absolute;
  right: 20px;
  bottom: 5px;
  background-image: url('../assets/search.svg');
}
</style>
  