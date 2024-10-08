<template>
  <div class="wrap">
    <form @submit.prevent="LoginClick"></form>
    <div class="login">
      <img src="../assets/Farmi.svg" alt="Logo" class="login-logo"><br>
      <div class="login_id">
        <h4>ID</h4>
        <input type="text" v-model="uid" placeholder="ID" class="input-field">
      </div>
      
      <div class="login_pw">
        <h4>Password</h4>
        <input type="password" v-model="upw" placeholder="Password" class="input-field">
      </div>
      
      <div class="signup">
        <p class="signup-text">
          <router-link to="/SignUpView">회원가입</router-link>
        </p>
      </div>

      <div class="submit">
        <button class="submit_button" @click="LoginClick">Login</button>
      </div>
    </div>
    <from />
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      uid: "",
      upw: "",
    };
  },
  methods: {
    async LoginClick() {
      try {
        // 서버에 POST 요청 보내기
        const response = await axios.post('/api/logincheck', {
          username: this.uid,
          password: this.upw,
        });

        // 서버 응답에 따른 처리
        if (response.data.success) {
          // 로그인 성공 시
          localStorage.setItem('loggedIn', true);
          this.$router.push('/MainView');
        } else {
          // 로그인 실패 시
          alert('로그인 실패: 아이디나 비밀번호가 잘못되었습니다.');
          localStorage.setItem('loggedIn', false);
          this.$router.push('/');
        }
      } catch (error) {
        // 서버 오류 발생 시
        alert('서버와의 통신 중 오류가 발생했습니다.');
        console.error(error);
        this.$router.push('/');
      }
    },
  },
};
</script>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: "Noto Sans KR", sans-serif;
  }
 
  .wrap {
    width: 100%;
    height: 100vh;           /* 뷰포트 높이의 100%, 즉 브라우저 창 전체 높이를 차지 */
    display: flex;
    align-items: center;     /* 수직 축에서 자식 요소를 중앙으로 정렬 */
    justify-content: center; /* 수평 축에서 자식 요소를 중앙으로 정렬 */
    background: rgba(0, 0, 0, 0.1);
  }
  
  .login {
    width: 80%; /* 화면 너비의 80% */
    height: auto;
    max-width: 300px; /* 최대 너비 */
    max-height: 1000vh;
    background: white;
    border-radius: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
    border: 3px solid #FA782D;
    box-sizing: border-box; /* 패딩 포함한 전체 크기 계산 */
}

.login-logo {
    width: 200px; /* 로고 크기를 상대적으로 설정 */
    max-width: 80%; /* 로고가 너무 커지지 않도록 */
    height: auto;
    margin-bottom: 20px;
    margin-top: 20px;
}

.login_id {
  width: 100%;
  margin-bottom: 20px;
}

.login_pw {
  width: 100%;
  margin-bottom: 10px;
}

h4 {
    margin: 0 0 5px 0;
}

.input-field {
    width: 100%; /* 입력 필드 너비를 100%로 설정 */
    padding: 10px;
    border: 2px solid #ddd;
    border-radius: 10px;
    font-size: 1rem;
    box-sizing: border-box; /* 패딩 포함한 전체 크기 계산 */
}

.submit {
    display: flex; /* Flexbox를 사용하여 중앙 정렬 */
    justify-content: center; /* 수평 중앙 정렬 */
    width: 50%; /* .submit 컨테이너가 부모 요소의 너비를 100% 사용하도록 설정 */
}

.submit_button {
    width: 100%;
    max-width: 300px; /* 최대 너비 */
    font-size: 1.35rem;
    background-color: #FA782D;
    color: white;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    margin-top: 10px;
    margin-bottom: 10px;
}

.submit_button:hover {
  background-color: #ff8a47;
}

.signup {
  margin-bottom: 5px;
  display: flex;
  justify-content: flex-end; /* 회원가입 버튼을 오른쪽으로 정렬 */
  width: 100%;
}

.signup-text {
  font-size: 13px;
  color: grey;
  text-decoration: underline;
  cursor: pointer;
}

.signup-text:hover {
  color: #FA782D; /* 마우스 오버 시 색상 변경 */
}

/* 반응형 디자인 */
@media (max-width: 768px) {
    .login {
        width: 90%; /* 작은 화면에서 너비 확장 */
        max-width: 300px;
    }

    .submit_button {
        font-size: 0.9rem;
    }
}

@media (max-width: 480px) {
    .login {
        width: 100%;
        padding: 15px;
    }

    .submit_button {
        font-size: 0.8rem;
    }
}

</style>