<template> <!--HTML짜는 곳-->
<LoginView />
  <header><img src="./assets/Farmi.svg" alt="farmi" height="50vh"></header>
  <button id="menu-button" v-if="isMobile" @click="toggleShow"></button>
  <nav class="menu">
    <div :id="isMobile ? 'nav-mobile' : 'nav-desktop'" >
      <ul v-if="show">
        <li><a href="#"></a>메인페이지</li>
        <li><a href="#"></a>병해진단</li>
        <li><a href="#"></a>챗봇</li>
        <li><a href="#"></a>환경그래프</li>
      </ul>
    </div>
    <div id="search_list">
    </div>
  </nav>
  <main class="main">
    <AppChatbot />
  </main>
</template>

<script>
import AppChatbot from './components/AppChatbot.vue';
import LoginView from './components/LoginView.vue';

 //JS짜는 곳
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
  components: {
    AppChatbot,
    LoginView,
  }
}
  
</script>

<style> /*CSS짜는 곳*/
body, html {
    margin: 0;
    height: 100vh;
}
header {
  border-bottom: 2px solid black;
  padding-left: 1.5vw;
}
nav {
  border-right: 1px solid gray;
}
ul {
  /*list-style-type: none;*/
  font-size: 125%;
}
li {
  padding: 5px;
}
a {
  text-decoration: none;
  color: inherit;
}
button {
  width: 35px;
  height: 35px;
  background-color: white;
  background-size: cover;
  border: none;
}
.menu, .main {
  display: inline-block;
}
.menu {
  float: left;
  background-color: snow;
}
.main {
  display: flex;
  justify-content: center; /* 가로축 중앙 정렬 */
  align-items: center; /* 세로축 중앙 정렬 */
  height: 100vh; /* 화면 전체 높이를 차지하도록 설정 */
  background-color: snow;
}
#menu-button {
  float: right;
  top: 5px;
  background-image: url('./assets/menu.svg');
}
</style>
