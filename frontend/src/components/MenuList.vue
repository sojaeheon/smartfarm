<template> <!--HTML짜는 곳-->
  <header><img src="../assets/Farmi.svg" alt="farmi" height="50vh"></header>
  <button id="menu-button" v-if="isMobile" @click="toggleShow"></button>
  <nav class="menu">
    <div :id="isMobile ? 'nav-mobile' : 'nav-desktop'" >
      <ul v-if="show">
        <li><router-link to="/">메인페이지</router-link></li>
        <li><router-link to="/DiseaseDiagnosis">병해진단</router-link></li>
        <li><router-link to="/AppChatbot">챗봇</router-link></li>
        <li><router-link to="/Graph">환경그래프</router-link></li>

        <!-- <li><a href="/">메인페이지</a></li>
        <li><a href="/DiseaseDiagnosis">병해진단</a></li>
        <li><a href="/AppChatbot">챗봇</a></li>
        <li><a href="/Graph">환경그래프</a></li> -->
      </ul>
    </div>
  </nav>
</template>

<script>

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
}
  
</script>

<style> /*CSS짜는 곳*/
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
.menu {
  display: inline-block;
  float: left;
  background-color: snow;
}
#menu-button {
  float: right;
  top: 5px;
  background-image: url('../assets/menu.svg');
}
</style>
