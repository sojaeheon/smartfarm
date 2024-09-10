<template> <!--HTML짜는 곳-->
  <header><img src="./assets/Farmi.svg" alt="farmi" height="50vh"></header>
  <nav class="menu">
    <button id="menu-button" v-if="isMobile" @click="toggleShow"></button>
    <div :id="{'nav-mobile': show}" >
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
    <div>
      <button id="search-list"></button>
    </div>
    <div id="chat">
      <div class="search">
        <AppChatbot />
      </div>
    </div>
  </main>
</template>

<script>
import AppChatbot from './components/AppChatbot.vue';

 //JS짜는 곳
export default{
  name: 'App',
  data(){
    return {
      show: true,
      isMobile: false,
      menuVisible: false 
    }
  },
  methods: {
    toggleShow(){
      this.show =! this.show;
    },
    checkIfMobile(){
      this.isMobile=window.innerWidth < 768;
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
    AppChatbot
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
  width: 40px;
  height: 40px;
  background-color: snow;
  background-size: cover;
  border: none;
}
.search{
  position: absolute;
  justify-content: center;
  bottom: 5vh;
  border: 2px solid blue;
}
.menu, .main {
  display: inline-block;
}
.menu {
  float: left;
  background-color: seashell;
}
.main {
  background-color: snow;
}
.bg-red {
  padding: 5px;
  text-align: center;
  color: white;
  background-color: #F99E17;
}
#menu-button {
  float: right;
  top: 5px;
  background-image: url('./assets/menu.svg');
}
#show {
  background-image: url('./assets/log-in.svg');
}
#search-list {
  position: fixed;
  top: 5px;
  right: 20px;
  background-image: url('./assets/settings.svg'); /*검색기록 이미지 찾기*/
}
</style>
