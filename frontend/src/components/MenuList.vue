<template> <!--HTML짜는 곳-->
  <header>
    <img src="../assets/Farmi.svg" alt="farmi" height="50vh">
    
    <div class="menuWrap">
      <button id="search-list"></button>
			<ul class="loginclick">
				<li><router-link to="/LoginView">로그인</router-link></li>
			</ul>
		</div>
  </header>
  <button id="menu-button" v-if="isMobile" @click="toggleShow"></button>
  <nav class="menu">
    <div :id="isMobile ? 'nav-mobile' : 'nav-desktop'" >
      <ul v-if="show">
        <li><router-link to="/">메인페이지</router-link></li>
        <li><router-link to="/DiseaseDiagnosis">병해진단</router-link></li>
        <li><router-link to="/AppChatbot">챗봇</router-link></li>
        <li><router-link to="/Graph">환경그래프</router-link></li>
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
  /* padding-left: 1.5vw; */

  display: flex;
  justify-content: space-between; /* 좌우로 아이템 배치 */
  align-items: center; /* 세로로 가운데 정렬 */
  padding: 5px 5px;
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
  color: #497132; /* 원하는 색상으로 변경 (로고 색에 맞춤)*/
  font-size: 0.8rem; /* 원하는 크기 조정 */
  padding: 3px 3px;  /* 내부 여백 */
  margin-top: 15px;
  margin-right: 60px;
  border: 2px solid #497132; /* 테두리 두께 */
  border-radius: 6px;
  transition: background-color 0.3s ease;
}

/* 로그인 링크 Hover 스타일 */
.loginclick a:hover {
  background-color: #497132;
  color: white;
}

#search-list {
  position: fixed;
  margin-top: 8px;
  background-image: url('../assets/settings.svg'); /*검색기록 이미지 찾기*/
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
