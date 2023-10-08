<template>
  <nav class="bg-[var(--tg-theme-bg-color)] px-4 py-2">
    <div class="flex items-center">
      <!-- Logo on the left side -->
      <div class="mr-4">
        <img src="/logo.png" alt="Logo" class="h-8">
      </div>

      <!-- Some space -->
      <div class="flex-1"></div>

      <!-- Menu items -->
      <div class="flex items-center gap-x-2">
        <nuxt-link active-class="rounded-lg bg-[var(--tg-theme-button-color)] text-[var(--tg-theme-button-text-color)]"
          to="/" class="py-1 px-2">
          📥 <span class="mr-2"></span> Inbox
        </nuxt-link>
        <nuxt-link active-class="rounded-lg bg-[var(--tg-theme-button-color)] text-[var(--tg-theme-button-text-color)]"
          to="/outbox" class="py-1 px-2">
          📨 <span class="mr-2"></span> Outbox
        </nuxt-link>
      </div>
    </div>
  </nav>
</template>
