<template>
    <div class="wrap">
      <form @submit.prevent="RegisterClick"> </form>
        <div class="register">
          <img src="../assets/Farmi.svg" alt="Logo" class="register-logo"><br>
        
          <div class="register_uid">
            <h4>ID</h4>
            <input type="text" v-model="uid" placeholder="uid" class="input-field">
          </div>

          <div class="register_pw">
            <h4>Password</h4>
            <input type="password" v-model="password" placeholder="Password" class="input-field">
          </div>

          <div class="register_rapa">
            <h4>Rapa_IP</h4>
            <input type="text" v-model="rapa_ip" placeholder="rapa_ip" class="input-field">
          </div>
            
          <div class="register_port">
            <h4>Port</h4>
            <input type="text" v-model="port" placeholder="port" class="input-field">
          </div>
      
      <div class="backlogin">
        <p class="backlogin-text">
          <router-link to="/">로그인</router-link>
        </p>
      </div>
      
      <div class="submit">
        <button class="submit_button" @click="RegisterClick">Sign Up</button>
      </div>
    </div>
  </div>
</template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        uid: "",
        password: "",
        rapa_ip: "",
        port : "",
      };
    },
    methods: {
      async RegisterClick() {
        try {
          // 서버에 POST 요청 보내기
          const response = await axios.post('/api/register', {
            uid: this.uid,
            password: this.password,
            rapa_ip: this.rapa_ip,
            port : this.port,
          });
  
          // 서버 응답에 따른 처리
          if (response.data.success) {
            // 회원가입 성공 시
            this.$router.push('/');  //로그인 창으로
          } else {
            // 회원가입 실패 시
            alert(response.data.message);
          }
        } catch (error) {
          // 서버 오류 발생 시
          alert('서버와의 통신 중 오류가 발생했습니다.');
          console.error(error);
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
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(0, 0, 0, 0.1);
    }
    
    .register {
      width: 80%;
      height: auto;
      max-width: 300px;
      background: white;
      border-radius: 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 20px;
      border: 3px solid #FA782D;
      box-sizing: border-box;
  }
  
  .register-logo {
      width: 200px;
      max-width: 80%;
      height: auto;
      margin-bottom: 20px;
      margin-top: 20px;
  }
  
  .register_uid, .register_rapa, .register_pw, .register_port {
      width: 95%;
      margin-bottom: 20px;
      margin-bottom: 20px;
  }
  
  h4 {
      margin: 0 0 5px 0;
  }
  
  .input-field {
      width: 100%;
      padding: 10px;
      border: 2px solid #ddd;
      border-radius: 10px;
      font-size: 1rem;
      box-sizing: border-box;
  }

  .backlogin {
  margin-bottom: 5px;
  display: flex;
  justify-content: flex-end; /* 회원가입 버튼을 오른쪽으로 정렬 */
  width: 100%;
}

.backlogin-text {
  font-size: 13px;
  color: grey;
  text-decoration: underline;
  cursor: pointer;
}

.backlogin-text:hover {
  color: #FA782D; /* 마우스 오버 시 색상 변경 */
}
  
.submit {
  display: flex;
    justify-content: center;
    width: 50%;
}
  
.submit_button {
  width: 100%;
  max-width: 300px;
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
  
@media (max-width: 768px) {
  .register {
    width: 90%;
    max-width: 325px;
  }
  .submit_button {
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .register {
    width: 100%;
    padding: 15px;
  }
  .submit_button {
    font-size: 0.8rem;
  }
}
</style>
  