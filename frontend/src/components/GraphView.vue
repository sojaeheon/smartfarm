<template>
  <header>
    <button id="menu-button" v-if="isMobile" @click="toggleShow"></button>
    <img src="../assets/Farmi.svg" alt="farmi" height="50vh">
    <div class="menuWrap">
      <ul class="loginclick">
        <li><router-link to="/LoginView">로그인</router-link></li>
      </ul>
    </div>
  </header>
  <div>
    <MenuList /> 
  </div>
  <h2>환경그래프</h2>
</template>

<script>

import MenuList from './MenuList.vue';
export default {
  name: 'GraphView',
  components: {
    MenuList
  },
};
</script>