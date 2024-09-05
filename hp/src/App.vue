<template> <!--HTML짜는 곳-->
  <aside class="menu" v-if="show">
    <div>
      <button id="hidden" @click="toggleShow"></button>
    </div>
    <div id="function">
      <p class="bg-red"><strong>기능들</strong></p>
      <ul>
        <li>챗봇</li>
        <li>병해충진단</li>
      </ul>
    </div>
    <div id="search_list">
      <p class="bg-red"><strong>검색 기록</strong></p>
    </div>
  </aside>
  <aside class="no-menu" v-else-if="!show">
    <button id=show @click="toggleShow"></button>
  </aside>
  <main class="main">
    <div>
      <button id="settings"></button>
    </div>
    <div id="chat">
      <div class="communicate">
        <textarea name="question"></textarea>
      </div>
      <p><strong>챗봇</strong></p>
      <div class="search">
        <input type="text" name="search_box" placeholder="무엇이 궁금하신가?">
        <button type="submit"></button>
      </div>
    </div>
  </main>
</template>

<script> //JS짜는 곳
export default{
  name: 'App',
  data(){
    return {
      show: true,
    }
  },
  methods: {
    toggleShow(){
      this.show=!this.show;
    }
  },
}
  
</script>

<style> /*CSS짜는 곳*/
body, html {
    margin: 0;
    display: flex;
    height: 100vh;
}
p {
  font-size: 1.5rem;
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
  top: 90vh;
  left: 30vw;
}
.search input{
  height: 5vh;
  width: 60vw;
  position: relative;
  padding: 0px 20px 0px 20px;
  font-size: 1rem;
  border-radius: 30px;
  border: 2px solid #F99E17;
}
.search button {
  position: absolute;
  right: 20px;
  top: 5px;
  background-image: url('./assets/search.svg');
}
.menu, .main {
  display: inline-block;
}
.menu {
  float: left;
  width: 17.5vw;
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
#hidden {
  float: right;
  top: 5px;
  background-image: url('./assets/log-out.svg');
}
#show {
  background-image: url('./assets/log-in.svg');
}
#function, #search_list, #chat {
  padding: 50px 0px;
  color: black;
}
#settings {
  position: fixed;
  top: 5px;
  right: 20px;
  background-image: url('./assets/settings.svg');
}
</style>
