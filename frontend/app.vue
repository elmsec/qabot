<template>
  <NuxtLayout>
    <NuxtLoadingIndicator />
    <Navbar />
    <NuxtPage />
    <div class="mb-8"></div>
  </NuxtLayout>
</template>

<script setup>
useHead(() => {
  return {
    link: [
      {
        rel: 'preconnect',
        href: 'https://fonts.googleapis.com'
      },
      {
        rel: 'preconnect',
        href: 'https://fonts.gstatic.com',
        crossorigin: true
      },
      {
        rel: 'stylesheet',
        href: 'https://fonts.googleapis.com/css2?family=Prompt:ital,wght@0,200;0,300;0,400;1,200;1,300;1,400&display=swap'
      }
    ]
  }
})

</script>

<style>
body {
  background-color: var(--tg-theme-secondary-bg-color);
  color: var(--tg-theme-text-color);
}
</style>
