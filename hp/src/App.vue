<template> <!--HTML짜는 곳-->
  <aside class="menu">
    <div>
      <img id="hidden" src="./assets/log-out.svg" alt="logout icon" />
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
  <main class="main">
    <div>
      <img id="settings" src="./assets/settings.svg" alt="settings icon" />
    </div>
    <div id="chat">
      <p><strong>챗봇</strong></p>
      <div class="search">
        <input type="text" name="search_box">
        <button type="submit"></button>
      </div>
    </div>
  </main>
</template>

<script> //JS짜는 곳


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
.search{
  position: absolute;
  top: 90vh;
  left: 30vw;
}
.search input{
  height: 5vh;
  width: 60vw;
  position: relative;
  padding: 0px 10px 0px 10px;

  border-radius: 30px;
  border: 2px solid #F99E17;
}
.search button {
  position: absolute;
  width: 40px;
  height: 40px;
  right: 20px;
  top: 5px;
  background-image: url('./assets/search.svg');
  background-color: snow;
  background-size: cover;
  border: none;
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
  float: right;
  width: 82.5vw;
  background-color: snow;
}
.bg-red {
  padding: 5px;
  text-align: center;
  color: white;
  background-color: #F99E17;
}
#function, #search_list, #chat {
  padding: 50px 0px;
  color: black;
}
#hidden, #settings {
  float: right;
}
</style>
