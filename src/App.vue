<template>
  <router-view v-slot="{ Component }">
    <transition name="scale" mode="out-in">
      <component :is="Component" />
    </transition>
  </router-view>
</template>


<script setup>
  //
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Victor+Mono:wght@400;700&display=swap');
  body {
      font-family: 'Victor Mono'
  }
  
  .scale-enter-active, .scale-leave-active {
    transition: all 0.5s ease;
  }

  .scale-enter-from, .scale-leave-to {
    opacity: 0;
    transform: scale(0.9);
  }


</style>