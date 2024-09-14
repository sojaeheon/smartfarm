<template>
  <nav class="menu">
    <div>
      <ul>
        <li><router-link to="/">메인페이지</router-link></li>
        <li><router-link to="/DiseaseDiagnosis">병해진단</router-link></li>
        <li><router-link to="/AppChatbot">챗봇</router-link></li>
        <li><router-link to="/Graph">환경그래프</router-link></li>
      </ul>
    </div>
  </nav>
</template>

<style>
nav {
  border-right: 1px solid gray;
}

ul {
  font-size: 125%;
  padding: 5px;
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
  width: 150px;
}

a:hover {
  color: #FA782D; /* 링크 Hover 효과 */
}

</style>