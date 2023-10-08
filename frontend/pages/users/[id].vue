<template>
  <div
    class="flex flex-col bg-[var(--tg-theme-secondary-bg-color)] h-full min-h-screen text-[var(--tg-theme-text-color)]">
    <div>
    </div>
    <div :key="questions" v-if="!error" class="rounded-lg shadow-md mt-4">
      <div class="m-4">
        <div class="mb-4">
          <h1 class="text-xl mb-1">{{ user.first_name }} <small>({{ user.link }})</small></h1>
          <h2 class="text-gray-300">Questions that the user has asked, along with their corresponding answers.</h2>
        </div>

        <QAPost v-if="questions && questions.length" :key="question" v-for="question in questions"
          :created="(new Date(question.created)).toLocaleString()" :text="question.text" :answer="question.answer" />
        <div v-else class="text-center justify-center flex flex-col m-4">
          No questions yet.
        </div>
      </div>
    </div>
    <div v-else>
      <p>Oops, something went wrong!</p>
      <p>{{ error }}</p>
      <button @click="refresh">Try again</button>
    </div>

    <QAForm v-if="isQuestionFormOpen" :title="`📨 Ask ${user.first_name} (${user.link}) a question`"
      v-model:isOpen="isQuestionFormOpen" v-model:text="questionText" @submitQAForm="submitQAForm"
      :progressing="progressing" :disabled="disabled" />

    <div v-else>
      <ClientOnly>
        <MainButton text="Ask new question 🚀" @click="openQuestionForm" />
      </ClientOnly>
    </div>
  </div>
  <BackButton @click="backPressed" />
</template>

<script setup>
import { MainButton, BackButton } from "vue-tg"
import { useTokenStore } from "@/store/token"

const tokenStore = useTokenStore()
const token = computed(() => tokenStore.token)

const runtimeConfig = useRuntimeConfig()
const apiBaseUrl = computed(() => runtimeConfig.public.apiBaseUrl)

const route = useRoute()
const router = useRouter()

const { data: user, error, refresh, pending } = await useFetch(`${apiBaseUrl.value}/users/${route.params.id}`)
const { data: questions, refresh: questionsRefresh } = await useFetch(`${apiBaseUrl.value}/users/${route.params.id}/inbox`)

const isQuestionFormOpen = ref(false)
const progressing = ref(false)
const disabled = ref(false)
const questionText = ref('')

const backPressed = () => {
  router.push('/')
}

const openQuestionForm = () => {
  isQuestionFormOpen.value = true
}

const submitQAForm = async () => {
  progressing.value = true
  disabled.value = true

  await new Promise((resolve) => setTimeout(resolve, 1000))

  await useFetch(`${apiBaseUrl.value}/users/${route.params.id}/inbox`, {
    method: 'POST',
    body: JSON.stringify({ text: questionText.value }),
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token.value}`
    }
  })

  isQuestionFormOpen.value = false
  progressing.value = false
  disabled.value = false


  questions.value = [
    {
      link: 'new-question',
      created: new Date().toLocaleString(),
      text: questionText.value,
      answer: null
    },
    ...questions.value
  ]

  questionText.value = ''
}


</script>
