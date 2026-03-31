<template>
  <n-config-provider :theme="darkTheme">
    <main>
      <router-view />
    </main>
  </n-config-provider>
</template>

<script>
import { NConfigProvider, darkTheme } from 'naive-ui';

export default {
  name: 'App',

  components: {
    NConfigProvider,
  },

  data() {
    return {
      darkTheme,
    };
  },
};
</script>

<style>
main {
  min-height: 100vh;
  padding: 20px;
  box-sizing: border-box;
}
</style>
