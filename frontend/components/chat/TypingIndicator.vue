<script setup lang="ts">
defineProps<{ label?: string }>()
</script>

<template>
  <div class="d-flex align-center gap-2 py-1">
    <div class="typing-dots"><span /><span /><span /></div>
    <span v-if="label" class="text-caption text-medium-emphasis">{{ label }}</span>
  </div>
</template>

<style scoped>
.typing-dots { display: flex; gap: 4px; align-items: center; }
.typing-dots span { width: 7px; height: 7px; border-radius: 50%; background: currentColor; opacity: 0.4; animation: bounce 1.2s infinite ease-in-out; }
.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce { 0%, 80%, 100% { transform: translateY(0); opacity: 0.4; } 40% { transform: translateY(-6px); opacity: 1; } }
</style>
