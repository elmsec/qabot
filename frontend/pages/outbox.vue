<template>
  <div class="flex flex-col bg-[var(--tg-theme-secondary-bg-color)] h-full min-h-screen">
    <main class="px-4">
      <h1 class="text-2xl text-center p-2 mt-2">👋 Hi, {{ user.first_name }}!</h1>
      <h2 class="text-lg">📨 <span class="mr-2"></span> Outbox</h2>

      <QAPost v-if="questions && questions.length" :key="question" v-for="question in questions"
        :created="(new Date(question.created)).toLocaleString()" :text="question.text" :answer="question.answer"
        @questionUpdated="questionUpdated" :link="question.link" />
      <div v-else class="text-center justify-center flex flex-col">
        <Vue3Lottie
          animationLink="https://assets-v2.lottiefiles.com/a/79f1d622-1163-11ee-9bfe-bfb9590c699a/zcCr6OrPJQ.json"
          :height="150" :width="150" />
        <div>
          <p class="text-md mb-2">No questions yet.</p>
          <p class="text-sm text-gray-200">
            Once you asked someone a question, our cat will wake up and ring the bell to inform that user on Telegram.
            You'll see the questions you asked here.
          </p>
        </div>
      </div>

    </main>
  </div>
</template>

<script setup>

import { computed } from "vue"
import { useWebApp } from "vue-tg"
import { Vue3Lottie } from 'vue3-lottie'
import { useInitDataStore } from "@/store/initData"
import { useLoadingStore } from "@/store/loading"
import { useTokenStore } from "@/store/token"

const initDataStore = useInitDataStore()
const loadingStore = useLoadingStore()
const tokenStore = useTokenStore()
const runtimeConfig = useRuntimeConfig()


const questionUpdated = (question) => {
  questions.value = questions.value.map((q) => {
    if (q.link === question.link) {
      return question
    }

    return q
  })
}


loadingStore.$patch({ loading: true })
const loading = computed(() => loadingStore.loading)

const { ready } = useWebApp()

const webApp = useWebApp()
initDataStore.setUser(webApp.initDataUnsafe.user)

await tokenStore.requestToken(webApp.initData)

ready()

const apiBaseUrl = computed(() => runtimeConfig.public.apiBaseUrl)

const { data: user } = await useFetch(
  `${apiBaseUrl.value}/users/me`,
  {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${tokenStore.token}`
    }
  },
)
const { data: questions } = await useFetch(
  `${apiBaseUrl.value}/users/me/outbox`,
  {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${tokenStore.token}`
    }
  },
)

loadingStore.$patch({ loading: false })

</script>

<style>
html {
  font-family: sans-serif;
  -webkit-text-size-adjust: 100%;
  -ms-text-size-adjust: 100%;
  -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
}
</style>
