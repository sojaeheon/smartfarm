<template>
    <div class="wrap">
          <div class="login">
              <h2 class="logo"></h2><br>
  
              <div class="login_id">
                  <h4>E-mail</h4>
                  <input type="email" name="" id="" placeholder="Email">
              </div>
  
              <div class="login_pw">
                  <h4>Password</h4>
                  <input type="password" name="" id="" placeholder="Password">
              </div>
              
              <div class="submit">
                <button class="submit_button" @click="LoginClick">submit</button>
              </div>
              
          </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        uid: "",
        upw: "",
      };
    },
    methods: {
      LoginClick(){
        console.log(this.uid, this.upw);
        alert('로그인 완료');
      }
    }
  };
  </script>
  
  <style>
  * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: "Noto Sans KR", sans-serif;
    }
  
    .logo {
      background-image: url('./assets/Farmi.svg');
      background-size: contain; /* 이미지가 요소에 맞게 조정 */
      background-repeat: no-repeat; /* 이미지 반복 방지 */
      background-position: left center; /* 배경 이미지의 위치 */
      padding-left: 50px; /* 텍스트와 이미지 사이의 간격 */
      line-height: 60px; /* 텍스트와 이미지의 수직 정렬 조정 */
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
      width: 30%;
      height: 600px;
      background: white;
      border-radius: 20px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-direction: column;
      border: 3px solid #FA782D;
    }
    
    h2 {
      color: #FA782D;
      font-size: 2em;
    }
    .login_sns {
      padding: 20px;
      display: flex;
    }
    
    .login_sns li {
      padding: 0px 15px;
    }
    
    .login_sns a {
      width: 50px;
      height: 50px;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 10px;
      border-radius: 50px;
      background: white;
      font-size: 20px;
      box-shadow: 3px 3px 3px rgba(0, 0, 0, 0.4), -3px -3px 5px rgba(0, 0, 0, 0.1);
    }
    
    .login_id {
      margin-top: 20px;
      width: 80%;
    }
    .login_id input {
      width: 100%;
      height: 50px;
      border-radius: 30px;
      margin-top: 10px;
      padding: 0px 20px;
      border: 1px solid lightgray;
      outline: none;
    }
    
    .login_pw {
      margin-top: 20px;
      width: 80%;
    }
    .login_pw input {
      width: 100%;
      height: 50px;
      border-radius: 30px;
      margin-top: 10px;
      padding: 0px 20px;
      border: 1px solid lightgray;
      outline: none;
    }
    
    .submit {
      margin-top: 50px;
      width: 80%;
    }
    .submit_button {
      position: grid; /* 브라우저 창을 기준으로 고정 */
      background-color: #FA782D; /* 버튼 배경색 */
      color: white; /* 버튼 글자 색 */
      border: none; /* 테두리 없음 */
      width: 100%;
      font-size: 23px; /* 글자 크기 */
      text-align: center;        /* 텍스트 가운데 정렬 */
      padding: 12px;        /* 내부 여백 */
      cursor: pointer;           /* 마우스 포인터 모양 변경 */
      border-radius: 12px;       /* 테두리 둥글게 */
    }
  </style>