<template>
  <nav class="menu">
    <div>
      <ul>
        <li><router-link to="/MainView">메인페이지</router-link></li>
        <li><router-link to="/DiseaseDiagnosis">병해진단</router-link></li>
        <li><router-link to="/AppChatbot">챗봇</router-link></li>
      </ul>
    </div>
    <div class="logout-container">
      <img src="../assets/log-out.svg" alt="" class="logout" @click="handleLogout">
    </div>
  </nav>
</template>

<script>
import axios from 'axios';

export default {
  methods: {
    async handleLogout() {
      try {
        // 서버에 로그아웃 요청 보내기
        const response = await axios.get('/api/logout');

        if (response.data.success) {
          localStorage.removeItem('loggedIn');  // 로컬 스토리지에서 로그인 상태 제거
          this.$router.push('/');          // 로그인 페이지로 이동
          alert('로그아웃 되었습니다.');
        } else {
          alert('로그아웃 실패');
        }
      } catch (error) {
        console.error('로그아웃 중 오류 발생:', error);
        alert('로그아웃 실패');
      }
    }
  }
};
</script>

<style>
nav {
  border-right: 1px solid gray;
}

ul {
  font-size: 125%;
  padding: 5px;
}

li {
  padding: 5px;
}

a {
  text-decoration: none;
  color: inherit;
}

.logout-container {
  display: flex;
  justify-content: flex-end;
  /* 오른쪽으로 정렬 */
  margin-right: 5px;
}

.logout {
  position: fixed;
  margin-top: 10px;
  margin-bottom: 10px;
  bottom: 0;
  width: 30px;
  cursor: pointer;
}

.menu {
  display: inline-block;
  float: left;
  background-color: rgb(251, 244, 244);
  width: 130px;
  height: 90vh;
}

a:hover {
  color: #FA782D;
  /* 링크 Hover 효과 */
}
</style>