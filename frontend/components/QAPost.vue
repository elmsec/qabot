<template>
  <div class="bg-[var(--tg-theme-bg-color)]  p-4 rounded-lg shadow-md mt-4 relative">
    <div v-if="canAnswer" class="absolute top-0 right-0 mt-2 mr-2">
      <button :disabled="deleting" class="rounded-lg bg-red-300 text-xs p-1"
        :class="deleting ? 'cursor-not-allowed opacity-60' : ''" @click="deleteRequested = true">
        <span v-if="!deleting">❌</span>
        <span v-else class="inline-block animate-spin">❌</span>
      </button>

      <Confirm v-if="deleteRequested" message="Are you sure you want to delete the question?"
        @close="handleConfirmDelete" />
    </div>

    <div class="mb-2">
      <p class="text-[var(--tg-theme-text-color)] font-semibold text-md">{{ text }}</p>
      <p class="text-[var(--tg-theme-text-color)] opacity-60 text-xs">{{ `Asked on ${created}` }}</p>
    </div>


    <div>
      <p v-if="answer" class="text-[var(--tg-theme-text-color)] text-md">{{ answer }}</p>
      <div v-else>
        <p class="text-[var(--tg-theme-text-color)] text-md italic">
          No answer yet.
        </p>
      </div>

      <div class="controls flex justify-end gap-x-4">
        <div v-if="canAnswer && !answer">
          <button
            class="text-[var(--tg-theme-button-text-color)] rounded-lg bg-[var(--tg-theme-button-color)] py-1 px-2 text-sm"
            @click="openQAForm">
            🚀 Answer
          </button>
        </div>

        <div v-if="canAnswer && answer">
          <button
            class="text-[var(--tg-theme-button-text-color)] rounded-lg bg-[var(--tg-theme-button-color)] py-1 px-2 text-sm"
            @click="() => openQAForm(answer)">
            ✍️ Edit
          </button>
        </div>
      </div>
    </div>
  </div>
  <QAForm :subtitle="`Question: ${text}`" v-if="isFormOpen" v-model:isOpen="isFormOpen" v-model:text="formText"
    @submitQAForm="submitForm" :progressing="progressing" :disabled="disabled" />
</template>

<script setup>
const props = defineProps(['link', 'created', 'text', 'answer', 'canAnswer'])
const emits = defineEmits(['questionUpdated', 'questionDeleted'])

import { useTokenStore } from "@/store/token"
import { Confirm } from 'vue-tg'

const isFormOpen = ref(false)
const progressing = ref(false)
const deleting = ref(false)
const disabled = ref(false)
const deleteRequested = ref(false)
const formText = ref('')

const handleConfirmDelete = (value) => {
  if (value) {
    deleteQuestion()
  }
  deleteRequested.value = false
}


const openQAForm = (value) => {
  isFormOpen.value = true

  if (typeof value === 'string') {
    formText.value = value
  }
}


const runtimeConfig = useRuntimeConfig()
const apiBaseUrl = computed(() => runtimeConfig.public.apiBaseUrl)
const tokenStore = useTokenStore()

const submitForm = async () => {
  progressing.value = true
  disabled.value = true

  await new Promise((resolve) => setTimeout(resolve, 1000))

  const { data: result, error } = await useFetch(`${apiBaseUrl.value}/questions/${props.link}/answer`, {
    method: 'PATCH',
    body: JSON.stringify({ answer: formText.value }),
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${tokenStore.token}`
    }
  })

  if (error.value) {
    console.error(error.value)
    progressing.value = false
    disabled.value = false
    return
  }
  console.log(result, 'result')

  const updatedQuestion = { ...props, answer: formText.value };
  emits('questionUpdated', updatedQuestion);

  isFormOpen.value = false
  progressing.value = false
  disabled.value = false
}

const deleteQuestion = async () => {
  deleting.value = true

  await new Promise((resolve) => setTimeout(resolve, 500))

  const { data: result, error } = await useFetch(`${apiBaseUrl.value}/questions/${props.link}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${tokenStore.token}`
    }
  })

  if (error.value) {
    console.error(error.value)
    deleting.value = false
    return
  }
  deleting.value = false

  emits('questionDeleted', props.link);
}
</script>
