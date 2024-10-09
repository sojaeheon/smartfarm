<template>
  <header class="header">
    <router-link to="/MainView">
      <img src="../assets/Farmi.svg" alt="farmi" class="logo" height="45vh"> <!--이미지를 클릭하면 메인페이지로-->
    </router-link>
    <button id="menu-button" v-if="isMobile" @click="toggleShow"></button>
  </header>
  <div class="menuWrap" v-if="show == true">
    <MenuList />
  </div>
</template>

<script>
import MenuList from '../components/MenuList.vue';

export default {
  name: 'AppHeader',
  data() {
    return {
      show: true,     // 메뉴 표시 여부 (모바일에서만 사용)
      isMobile: false, // 현재 화면이 모바일인지 확인
    };
  },
  methods: {
    toggleShow() {
      this.show = !this.show;
    },
    checkIfMobile() {
      this.isMobile = window.innerWidth < 768;  // 모바일 화면 크기 체크
      if (!this.isMobile) {
        this.show = true;  // PC에서는 항상 메뉴가 보여야 함
      } else {
        this.show = false; // 모바일에서는 숨김 상태로 시작
      }
    },
  },
  mounted() {
    this.checkIfMobile();
    window.addEventListener('resize', this.checkIfMobile);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.checkIfMobile);
  },
  components: {
    MenuList,
  }
};
</script>

<style>
.header {
  border-bottom: 2px solid black;
  display: flex;
  justify-content: center;
  /* 로고를 가운데로 배치 */
  align-items: center;
  /* 세로로 가운데 정렬 */
  padding: 8px;
  position: relative;
  /* 메뉴 버튼이 위치할 수 있도록 설정 */
}

#menu-button {
  background-image: url('../assets/menu.svg');
  background-size: contain;
  background-repeat: no-repeat;
  width: 30px;
  height: 30px;
  border: none;
  cursor: pointer;
  position: absolute;
  left: 20px;
  /* 헤더 왼쪽에 위치 */
}

.logo {
  position: relative;
  /* 가운데 정렬을 위한 설정 */
}

.nav-bar {
  display: flex;
  width: 200px;
  height: 100%;

}

.nav-bar.open {
  transform: translateX(0);
}

/* 모바일 화면에서 메뉴 버튼만 보이도록 설정 */
@media (min-width: 768px) {
  #menu-button {
    display: none;
    /* 모바일 화면에서만 보이도록 설정 */
  }

  .nav-bar {
    transform: translateX(0);
    /* PC 화면에서는 항상 보이게 설정 */
  }
}
</style>