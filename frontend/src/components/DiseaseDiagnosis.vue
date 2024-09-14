<template>
    <header>
        <div>
            <AppHeader />
        </div>
    </header>
    <div class="PhotoSelection">
        <button class="Selection">사진 선택..</button>

    </div>
</template>

<script>
import AppHeader from './AppHeader.vue';

export default {
    data() {
        return{

        }
    },
    components: {
        AppHeader
    },
}

</script>

<style>
.PhotoSelection {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 80vh;
}
.Selection {
    background-color: #f0f0f0;
    border-radius: 10px;
    font-size: 20px;
    width: 55%;
    height: 55%;
    cursor: pointer;
}
</style>