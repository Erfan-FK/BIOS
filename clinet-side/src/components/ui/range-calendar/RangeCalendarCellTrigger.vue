<script setup>
import { buttonVariants } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { RangeCalendarCellTrigger, useForwardProps } from 'radix-vue';
import { computed } from 'vue';

const props = defineProps({
  day: { type: null, required: true },
  month: { type: null, required: true },
  asChild: { type: Boolean, required: false },
  as: { type: null, required: false },
  class: { type: null, required: false },
});

const delegatedProps = computed(() => {
  const { class: _, ...delegated } = props;

  return delegated;
});

const forwardedProps = useForwardProps(delegatedProps);
</script>

<template>
  <RangeCalendarCellTrigger
    :class="
      cn(
        buttonVariants({ variant: 'ghost' }),
        'h-9 w-9 p-0 font-normal data-[selected]:opacity-100',
        '[&[data-today]:not([data-selected])]:bg-gray-100 [&[data-today]:not([data-selected])]:text-gray-900 dark:[&[data-today]:not([data-selected])]:bg-gray-800 dark:[&[data-today]:not([data-selected])]:text-gray-50',
        // Selection Start
        'data-[selection-start]:bg-gray-900 data-[selection-start]:text-gray-50 data-[selection-start]:hover:bg-gray-900 data-[selection-start]:hover:text-gray-50 data-[selection-start]:focus:bg-gray-900 data-[selection-start]:focus:text-gray-50 dark:data-[selection-start]:bg-gray-50 dark:data-[selection-start]:text-gray-900 dark:data-[selection-start]:hover:bg-gray-50 dark:data-[selection-start]:hover:text-gray-900 dark:data-[selection-start]:focus:bg-gray-50 dark:data-[selection-start]:focus:text-gray-900',
        // Selection End
        'data-[selection-end]:bg-gray-900 data-[selection-end]:text-gray-50 data-[selection-end]:hover:bg-gray-900 data-[selection-end]:hover:text-gray-50 data-[selection-end]:focus:bg-gray-900 data-[selection-end]:focus:text-gray-50 dark:data-[selection-end]:bg-gray-50 dark:data-[selection-end]:text-gray-900 dark:data-[selection-end]:hover:bg-gray-50 dark:data-[selection-end]:hover:text-gray-900 dark:data-[selection-end]:focus:bg-gray-50 dark:data-[selection-end]:focus:text-gray-900',
        // Outside months
        'data-[outside-view]:text-gray-500 data-[outside-view]:opacity-50 [&[data-outside-view][data-selected]]:bg-gray-100/50 [&[data-outside-view][data-selected]]:text-gray-500 [&[data-outside-view][data-selected]]:opacity-30 dark:data-[outside-view]:text-gray-400 dark:[&[data-outside-view][data-selected]]:bg-gray-800/50 dark:[&[data-outside-view][data-selected]]:text-gray-400',
        // Disabled
        'data-[disabled]:text-gray-500 data-[disabled]:opacity-50 dark:data-[disabled]:text-gray-400',
        // Unavailable
        'data-[unavailable]:text-gray-50 data-[unavailable]:line-through dark:data-[unavailable]:text-gray-50',
        props.class,
      )
    "
    v-bind="forwardedProps"
  >
    <slot />
  </RangeCalendarCellTrigger>
</template>
