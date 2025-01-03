<script setup>
import Header from './components/Header.vue'
import { Toaster } from '@/components/ui/sonner'
</script>

<template>
    <Header />
    <Toaster />
    <router-view />
    <Toaster />
</template>
  

