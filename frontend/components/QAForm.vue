<template>
  <ModalBackdrop :isActive="isOpen" @update:isActive="onCancel" />

  <div v-if="isOpen" class="fixed bottom-0 left-0 w-full rounded-xl z-50">
    <div class="relative bg-[var(--tg-theme-secondary-bg-color)] p-4 rounded-t-3xl">
      <h1 class="text-lg text-center">{{ title }}</h1>
      <p>{{ subtitle }}</p>

      <textarea :value="text" @input="$emit('update:text', $event.target.value)" :disabled="progressing"
        class="w-full h-24 mt-4 p-2 rounded-lg shadow-md bg-[var(--tg-theme-bg-color)]"
        :placeholder="placeholder"></textarea>

      <div class="flex justify-end mt-4">
        <ClientOnly>
          <MainButton :progress="progressing" :disabled="disabled" :text="mainButtonText"
            @click="$emit('submitQAForm', text)" />
          <BackButton @click="onCancel" />
        </ClientOnly>
      </div>
    </div>

  </div>
</template>

<script setup>
const props = defineProps({
  title: String,
  subtitle: String,
  placeholder: String,
  text: String,
  isOpen: Boolean,
  progressing: Boolean,
  disabled: Boolean,
})
const emits = defineEmits(['update:isOpen', 'update:text', 'submitQAForm'])

import { MainButton, BackButton, useWebAppViewport } from "vue-tg"

const { isExpanded, expand } = useWebAppViewport()

if (!isExpanded.value) {
  expand()
}

const onCancel = () => {
  emits('update:isOpen', false)
  emits('update:text', '')
}

const mainButtonText = computed(() => {
  if (props.progressing) {
    return 'Sending...'
  }

  return 'Send 🚀🚀🚀'
})

</script>
