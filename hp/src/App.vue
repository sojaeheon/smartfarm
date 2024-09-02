<template> <!--HTML짜는 곳-->
  <aside class="menu">
    <div>
      <img id="hidden" src="./assets/log-out.svg" />
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
  <article class="main">
    <div>
      <img id="setting" src="./assets/settings.svg" />
    </div>
    <div id="chat">
      <p><strong>챗봇</strong></p>
      <span class="search"><input type="text" value=""></span>
    </div>
  </article>
</template>

<script> //JS짜는 곳


</script>

<style> /*CSS짜는 곳*/
body, html {
    margin: 0;
    display: flex;
}
p {
  font-size: 1.5rem;
}
.search input{ 
  height: 5vh;
  width: 50vw;
  position: absolute;
  top: 90vh;
  left: 30vw;
  margin: 1px 2px 3px 4px;

  border-radius: 30px;
  border: 2px solid #F99E17;
}
.menu, .main {
  display: inline-block;
}
.menu {
  float: left;
  height: 100vh;
  width: 14.5vw;
  background-color: seashell;
}
.main {
  float: right;
  height: 100vh;
  width: 84.5vw;
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
#hidden, #setting {
  float: right;
}
</style>
