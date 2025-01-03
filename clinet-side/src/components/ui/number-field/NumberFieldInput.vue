<script setup>
import { cn } from '@/lib/utils';
import { NumberFieldInput } from 'radix-vue';

const props = defineProps({
  class: { type: null, required: false },
});
</script>

<template>
  <NumberFieldInput
    data-slot="input"
    :class="
      cn(
        'flex h-10 w-full rounded-md border border-gray-200 bg-white py-2 text-sm text-center ring-offset-white placeholder:text-gray-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-950 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 dark:border-gray-800 dark:bg-gray-950 dark:ring-offset-gray-950 dark:placeholder:text-gray-400 dark:focus-visible:ring-gray-300',
        props.class,
      )
    "
  />
</template>
