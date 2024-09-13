<template> <!--HTML짜는 곳-->
  <button id="menu-button" v-if="isMobile" @click="toggleShow"></button>
  <nav class="menu" :id="isMobile ? 'nav-mobile' : 'nav-desktop'">
    <ul v-if="show">
      <li><a href="/">메인페이지</a></li>
      <li><a href="#">병해진단</a></li>
      <li><a href="/AppChatbot">챗봇</a></li>
      <li><a href="#">환경그래프</a></li>
    </ul>
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
nav {
  padding: 2vw 1.5vw 1vw 1.5vw;
}
ul {
  list-style-type: none;
  font-size: 125%;
}
li {
  padding: 0vw 1vw 1.5vw 0vw;
}
a {
  text-decoration: none;
  color: inherit;
}
.menu {
  display: inline-block;
}
#menu-button {
  float: right;
  top: 5px;
  background-image: url('../assets/menu.svg');
}
</style>