<template>
  <div class="flex flex-col bg-[var(--tg-theme-secondary-bg-color)] h-full min-h-screen ">
    <main class="px-4">
      <h1 class="text-2xl text-center p-2 mt-2">👋 Hi, {{ user.first_name }}!</h1>
      <h2 class="text-lg">📥 <span class="mr-2"></span> Inbox</h2>

      <QAPost v-if="questions && questions.length" :key="question" v-for="question in questions"
        :created="(new Date(question.created)).toLocaleString()" :text="question.text" :answer="question.answer"
        @questionUpdated="questionUpdated" @questionDeleted="questionDeleted" :link="question.link" :can-answer="true" />
      <div v-else class="text-center justify-center flex flex-col">
        <Vue3Lottie
          animationLink="https://assets-v2.lottiefiles.com/a/79f1d622-1163-11ee-9bfe-bfb9590c699a/zcCr6OrPJQ.json"
          :height="150" :width="150" />
        <div>
          <p class="text-md mb-2">No questions yet. </p>
          <p class="text-sm text-[var(--tg-theme-text-color)]">
            Once someone asks you a question, our cat will wake up and ring the bell to inform you on Telegram.
          </p>

          <div class="bg-[var(--tg-theme-bg-color)] p-2 mt-8 text-sm rounded-xl">
            <p class="">Share your link and let the world ask you anything anonymously!
            </p>
            <!-- A div with link text with css select-all, and also a button to copy the text on click -->
            <div class="flex items-center justify-center gap-x-2 mt-2">
              <div class="select-all bg-[var(--tg-theme-bg-color)] py-1 px-2 rounded-lg">
                https://t.me/{{ runtimeConfig.public.botUsername }}?start={{ user.link }}
              </div>
            </div>
          </div>

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

const questionDeleted = (questionLink) => {
  questions.value = questions.value.filter((q) => q.link !== questionLink)
}


loadingStore.$patch({ loading: true })
const loading = computed(() => loadingStore.loading)

const { ready } = useWebApp()

const webApp = useWebApp()

if (webApp.initDataUnsafe.start_param && !initDataStore.user.id) {
  const userLink = webApp.initDataUnsafe.start_param
  navigateTo(`/users/${userLink}`, { replace: true })
}

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
  `${apiBaseUrl.value}/users/me/inbox`,
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
