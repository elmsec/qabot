<template>
  <div v-if="isActive" @click="$emit('update:isActive', false)"
    class="bg-gray-900 bg-opacity-90 dark:bg-opacity-80 fixed inset-0 z-40">
  </div>
</template>

<script setup>
defineProps(['isActive'])
defineEmits(['update:isActive'])
</script>
