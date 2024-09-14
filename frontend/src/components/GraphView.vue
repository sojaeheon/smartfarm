<template>
  <header>
      <div>
          <AppHeader />
      </div>
  </header>
  <h2>환경그래프</h2>
</template>

<script>

import AppHeader from './AppHeader.vue';
export default {
  name: 'GraphView',
  components: {
    AppHeader
  },
};
</script>