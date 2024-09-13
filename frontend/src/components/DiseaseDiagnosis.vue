<template>
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


</style>