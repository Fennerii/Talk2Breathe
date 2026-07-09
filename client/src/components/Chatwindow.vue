<script setup>
import { ref, onMounted, nextTick } from 'vue'

const props = defineProps({
  initialMessage: String
})

const emit = defineEmits(['reset'])

const messages = ref([])
const newMessage = ref('')
const isLoading = ref(false)
const sessionId = crypto.randomUUID()
const chatBody = ref(null)

const colors = ['#1b75bc', '#39b54a', '#fbb03b', '#ff1d25', '#4d4d4d', '#ffffff']
const dots = Array.from({ length: 60 }, () => ({
  top: Math.random() * 100,
  left: Math.random() * 100,
  size: 10 + Math.random() * 6,
  color: colors[Math.floor(Math.random() * colors.length)],
  duration: 8 + Math.random() * 12,
  delay: Math.random() * -20
}))

async function sendToBackend(text) {
  messages.value.push({ role: 'user', text })
  isLoading.value = true
  await scrollToBottom()

  try {
    const res = await fetch('http://localhost:8000/api/v1/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text, session_id: sessionId })
    })
    const data = await res.json()
    messages.value.push({ role: 'bot', text: data.response })
  } catch (error) {
    messages.value.push({ role: 'bot', text: 'Sorry, something went wrong. Please try again.' })
    console.error('Chat error:', error)
  } finally {
    isLoading.value = false
    await scrollToBottom()
  }
}

async function scrollToBottom() {
  await nextTick()
  if (chatBody.value) {
    chatBody.value.scrollTop = chatBody.value.scrollHeight
  }
}

function sendMessage() {
  if (!newMessage.value.trim() || isLoading.value) return
  sendToBackend(newMessage.value)
  newMessage.value = ''
}

onMounted(() => {
  if (props.initialMessage) {
    sendToBackend(props.initialMessage)
  }
})
</script>

<template>
  <section class="hero is-fullheight particle-bg">
    <div
      v-for="(dot, i) in dots"
      :key="i"
      class="dot"
      :style="{
        top: dot.top + '%',
        left: dot.left + '%',
        width: dot.size + 'px',
        height: dot.size + 'px',
        backgroundColor: dot.color,
        animationDuration: dot.duration + 's',
        animationDelay: dot.delay + 's'
      }"
    />

    <div class="hero-body">
      <div class="container">
        <div class="columns is-vcentered is-centered cards-row">
          <div class="column is-narrow">
            <div class="glass-card chat-box">

              <!-- Top bar -->
              <div class="top-bar">
                <span class="chat-title">Talking with Breathe</span>
                <button class="new-chat-btn" @click="emit('reset')">
                  <span>New Chat</span>
                  <i class="fa-solid fa-plus"></i>
                </button>
              </div>

              <!-- Messages -->
              <div class="chat-body" ref="chatBody">
                <div
                  v-for="(msg, i) in messages"
                  :key="i"
                  :class="['message-row', msg.role]"
                >
                  <div class="bubble">{{ msg.text }}</div>
                </div>

                <!-- Loading indicator -->
                <div v-if="isLoading" class="message-row bot">
                  <div class="bubble loading">
                    <span>.</span><span>.</span><span>.</span>
                  </div>
                </div>
              </div>

              <!-- Input bar -->
              <div class="input-bar">
                <form @submit.prevent="sendMessage" class="input-row">
                  <input
                    v-model="newMessage"
                    type="text"
                    class="chat-input"
                    placeholder="Ask Breathe something..."
                    :disabled="isLoading"
                  />
                  <button type="submit" class="send-btn" :disabled="isLoading">
                    <i class="fa-solid fa-paper-plane"></i>
                  </button>
                </form>
              </div>

            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.particle-bg {
  background-color: #ffffff;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.dot {
  position: absolute;
  border-radius: 50%;
  opacity: 0.7;
  pointer-events: none;
  animation-name: float;
  animation-timing-function: ease-in-out;
  animation-iteration-count: infinite;
}

@keyframes float {
  0%   { transform: translate(0, 0); }
  25%  { transform: translate(15px, -20px); }
  50%  { transform: translate(-10px, -35px); }
  75%  { transform: translate(-20px, -10px); }
  100% { transform: translate(0, 0); }
}

.cards-row {
  position: relative;
  z-index: 1;
}

.glass-card {
  backdrop-filter: blur(20px);
  background: rgba(255, 255, 255, 0.35);
  border: 2px solid #9daecc;
  border-radius: 24px;
  box-shadow: 0 4px 12px #01050b;
}

.chat-box {
  width: 910px;
  height: 780px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #9daecc;
  padding: 16px 24px;
  flex-shrink: 0;
}

.chat-title {
  font-weight: 600;
  color: #1a1a1a;
}

.new-chat-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border-radius: 999px;
  border: 1px solid grey;
  padding: 10px 18px;
  background-color: lightgray;
  cursor: pointer;
  font-size: 14px;
}

.chat-body {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message-row {
  display: flex;
}

.message-row.user {
  justify-content: flex-end;
}

.message-row.bot {
  justify-content: flex-start;
}

.bubble {
  max-width: 65%;
  padding: 12px 16px;
  border-radius: 18px;
  font-size: 14px;
  line-height: 1.6;
  color: #1a1a1a;
}

.message-row.user .bubble {
  background: #1b75bc;
  color: white;
  border-bottom-right-radius: 4px;
}

.message-row.bot .bubble {
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid #9daecc;
  border-bottom-left-radius: 4px;
}

.loading span {
  animation: blink 1.2s infinite;
  font-size: 20px;
  line-height: 1;
}

.loading span:nth-child(2) { animation-delay: 0.2s; }
.loading span:nth-child(3) { animation-delay: 0.4s; }

@keyframes blink {
  0%, 80%, 100% { opacity: 0; }
  40% { opacity: 1; }
}

.input-bar {
  border-top: 1px solid #9daecc;
  padding: 16px 24px;
  flex-shrink: 0;
}

.input-row {
  display: flex;
  gap: 8px;
  align-items: center;
}

.chat-input {
  flex: 1;
  padding: 10px 16px;
  border-radius: 999px;
  border: 1px solid #9daecc;
  background: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  outline: none;
}

.chat-input:disabled {
  opacity: 0.6;
}

.send-btn {
  background: #1b75bc;
  color: white;
  border: none;
  border-radius: 999px;
  width: 40px;
  height: 40px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>