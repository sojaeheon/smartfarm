<template>
  <div class="wrap">
    <form @submit.prevent="RegisterClick"> </form>
    <div class="register">
      <img src="../assets/Farmi.svg" alt="Logo" class="register-logo"><br>

      <div class="register_uid">
        <h4>ID</h4>
        <div class="uid-row">
          <input type="text" v-model="uid" placeholder="ID" class="input-field">
          <button class="check-duplicate" @click="checkDuplicateUid">중복 확인</button>
        </div>
        <span v-if="isUidAvailable" class="available">사용 가능한 아이디입니다.</span>
        <span v-if="!isUidAvailable && uidChecked" class="not-available">이미 사용 중인 아이디입니다.</span> -->
      </div>

      <div class="register_pw">
        <h4>Password</h4>
        <input type="password" v-model="password" placeholder="Password" class="input-field">
      </div>

      <div class="device_name">
        <h4>Device_name</h4>
        <input type="text" v-model="device_name" placeholder="Rapa_ip" class="input-field">
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
      device_name: "",
      isUidAvailable: false,
      uidChecked: false,
    };
  },
  methods: {
    // 아이디 중복 확인
    async checkDuplicateUid() {
      if (!this.uid) {
        alert('아이디를 입력하세요.');
        return;
      }
      try {
        const response = await axios.post('/api/check-uid', { uid: this.uid });
        if (response.data.available) {
          this.isUidAvailable = true;
          this.uidChecked = true;
          alert('사용 가능한 아이디입니다.');
        } else {
          this.isUidAvailable = false;
          this.uidChecked = true;
          alert('이미 사용 중인 아이디입니다.');
        }
      } catch (error) {
        alert('서버와의 통신 중 오류가 발생했습니다.');
        console.error(error);
      }
    },
    async RegisterClick() {
      try {
        // 서버에 POST 요청 보내기
        const response = await axios.post('/api/register', {
          uid: this.uid,
          password: this.password,
          device_name: this.device_name,
        });

        if (response.data.success) {
          // 회원가입 성공 시
          alert(response.data.message)
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

.register_uid,
.device_name,
.register_pw {
  width: 95%;
  margin-bottom: 20px;
}

.uid-row {
  display: flex;
  justify-content: flex-start;
  /* 왼쪽 정렬 */
  align-items: center;
  width: 100%;
  /* 너비를 100%로 설정 */
  gap: 10px;
  /* 입력 필드와 버튼 간 간격 설정 */
}

h4 {
  margin: 0;
}

.check-duplicate {
  width: 25%;
  background-color: transparent;
  color: grey;
  border: 1px solid grey;
  padding: 8px 12px;
  /* 버튼의 padding을 조절하여 크기를 적당히 설정 */
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
  font-size: 50%;
  /* 글씨 크기를 줄임 */
  display: flex;
  justify-content: center;
  /* 수평 중앙 정렬 */
  align-items: center;
  /* 수직 중앙 정렬 */
}

.check-duplicate:hover {
  background-color: #FA782D;
  color: white;
  font-size: 50%;
}

.input-field {
  flex-grow: 1;
  padding: 10px;
  border: 2px solid #ddd;
  border-radius: 10px;
  font-size: 1rem;
  box-sizing: border-box;
}

.backlogin {
  margin-bottom: 5px;
  display: flex;
  justify-content: flex-end;
  width: 100%;
}

.backlogin-text {
  font-size: 13px;
  color: grey;
  text-decoration: underline;
  cursor: pointer;
}

.backlogin-text:hover {
  color: #FA782D;
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