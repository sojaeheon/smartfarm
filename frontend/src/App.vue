<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default{
  name: 'App',
  created() {
    // 여기에 로그인 상태 확인 로직을 추가할 수 있습니다.
    const isLoggedIn = localStorage.getItem('loggedIn');
    if (!isLoggedIn) {
      this.$router.push('/LoginView');
    } else {
      this.$router.push('/MainView');
    }
  }
}
</script>

<style> /*CSS짜는 곳*/
button {
  width: 35px;
  height: 35px;
  background-color: white;
  background-size: cover;
  border: none;
}
</style>