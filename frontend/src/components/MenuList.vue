<template>
  <!-- <header>
    <button id="menu-button" v-if="isMobile" @click="toggleShow"></button>
    <img src="../assets/Farmi.svg" alt="farmi" height="50vh">
    
    <div class="menuWrap">
      <ul class="loginclick">
        <li><router-link to="/LoginView">로그인</router-link></li>
      </ul>
    </div>
  </header> -->

  <nav class="menu">
    <div :id="isMobile ? 'nav-mobile' : 'nav-desktop'">
      <ul v-if="show">
        <li><router-link to="/">메인페이지</router-link></li>
        <li><router-link to="/DiseaseDiagnosis">병해진단</router-link></li>
        <li><router-link to="/AppChatbot">챗봇</router-link></li>
        <li><router-link to="/Graph">환경그래프</router-link></li>
      </ul>
    </div>
  </nav>
</template>

<script> //JS짜는 곳
export default{
name: 'App',
data(){
 return {
   show: true,
   isMobile: false
 }
},
methods: {
 toggleShow(){
   this.show =! this.show;
 },
 checkIfMobile() {
   this.isMobile = window.innerWidth < 768;  // 화면 크기에 따라 모바일 여부 판단
   if (!this.isMobile) {
     this.show = true;  // PC에서는 항상 메뉴가 보여야 함
   } else {
     this.show = false; // 모바일에서는 숨김 상태로 시작
   }
 }
},
mounted() {
 this.checkIfMobile();
 window.addEventListener('resize', this.checkIfMobile);
},
beforeUnmount() {
 window.removeEventListener('resize', this.checkIfMobile);
},
}

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

#menu-button {
background-image: url('../assets/menu.svg');
background-size: contain;
background-repeat: no-repeat;
width: 30px;
height: 30px;
border: none;
cursor: pointer;
margin-left: 10px; /* 왼쪽에 여백을 추가 */
}

header img {
position: absolute;
left: 50%;
transform: translateX(-50%); /* 가운데 정렬 */
}

.menuWrap {
display: flex;
align-items: center;
justify-content: flex-end; /* 오른쪽 정렬 */
margin-right: 10px; /* 오른쪽에 약간의 여백 추가 */
}

.loginclick {
list-style: none;
margin: 0;
padding: 0;
}

.loginclick li {
display: inline-block;
}

.loginclick a {
text-decoration: none;
color: #497132;
font-size: 0.8rem;
padding: 3px 8px;
border: 2px solid #497132;
border-radius: 6px;
transition: background-color 0.3s ease;
margin-left: 15px;
}

.loginclick a:hover {
background-color: #497132;
color: white;
}

/* #search-list {
background-image: url('../assets/settings.svg');
background-size: cover;
width: 30px;
height: 30px;
border: none;
margin-left: 15px;
cursor: pointer;
} */

nav {
border-right: 1px solid gray;
}

ul {
font-size: 125%;
}

li {
padding: 5px;
}

a {
text-decoration: none;
color: inherit;
}

.menu {
display: inline-block;
float: left;
background-color: snow;
}

</style>