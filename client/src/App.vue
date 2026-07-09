<script setup>
import { ref } from 'vue'
import StartScreen from './components/Startscreen.vue'
import ChatWindow from './components/Chatwindow.vue'

const chatStarted = ref(false)
const firstMessage = ref('')

function startChat(message) {
  firstMessage.value = message
  chatStarted.value = true
}
</script>

<template>
  <StartScreen v-if="!chatStarted" @start-chat="startChat" />
  <ChatWindow v-else :initial-message="firstMessage" @reset="chatStarted = false" />
</template>