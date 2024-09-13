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
</template>

<script>
import MenuList from '../components/MenuList.vue';

export default {
    data() {
        return{

        }
    },
    method: {
        병해진단클릭() {
            this.$router.push('/MainVIew');
        },
    },
    components: {
        MenuList
    },
}

</script>

<style>
header {
border-bottom: 2px solid black;
display: flex;
justify-content: space-between; /* 좌우로 아이템 배치 */
align-items: center; /* 세로로 가운데 정렬 */
padding: 12px;
position: fiexed;
}

</style>