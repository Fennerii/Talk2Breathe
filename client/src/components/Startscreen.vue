<script setup>
import { ref } from 'vue'

const emit = defineEmits(['start-chat'])
const message = ref('')

const colors = ['#1b75bc', '#39b54a', '#fbb03b', '#ff1d25', '#4d4d4d', '#ffffff']
const dots = Array.from({ length: 60 }, () => ({
  top: Math.random() * 100,
  left: Math.random() * 100,
  size: 10 + Math.random() * 6,
  color: colors[Math.floor(Math.random() * colors.length)],
  duration: 8 + Math.random() * 12,
  delay: Math.random() * -20
}))

function handleSubmit() {
  if (!message.value.trim()) return
  emit('start-chat', message.value)
  message.value = ''
}
</script>

<template>
  <section class="page">
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

    <div class="cards-row">

      <div class="glass-card name-card">
        <h1 class="brand-title">Talk2Breathe</h1>
        <p class="brand-sub">Your friendly guide to a smoke-free life</p>
      </div>

      <div class="glass-card input-card">
        <p class="input-label">Ask Breathe anything about smoking and health</p>
        <form @submit.prevent="handleSubmit" class="input-row">
          <input
            v-model="message"
            type="text"
            class="chat-input"
            placeholder="Why is smoking bad for me?"
            autofocus
          />
          <button type="submit" class="send-btn">➤</button>
        </form>
      </div>

    </div>
  </section>
</template>

<style scoped>
* { box-sizing: border-box; }

.page {
  width: 100vw;
  height: 100vh;
  background-color: #ffffff;
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
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 32px;
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

.name-card {
  width: 380px;
  height: 560px;
  padding: 40px 32px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.brand-title {
  font-size: 2.5rem;
  font-weight: 700;
  font-family: monospace;
  color: #1a1a1a;
  text-align: center;
  margin-bottom: 16px;
}

.brand-sub {
  font-size: 1rem;
  color: #444;
  text-align: center;
}

.input-card {
  width: 320px;
  padding: 32px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.input-label {
  font-size: 14px;
  color: #444;
  text-align: center;
}

.input-row {
  display: flex;
  gap: 8px;
  align-items: center;
}

.chat-input {
  flex: 1;
  padding: 10px 14px;
  border-radius: 999px;
  border: 1px solid #9daecc;
  background: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  outline: none;
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
  font-size: 16px;
}
</style>