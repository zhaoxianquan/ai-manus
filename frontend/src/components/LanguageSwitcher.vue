<template>
  <div className="language-switcher">
  
    <select
      v-model="currentLocale"
      className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
    >
      <option v-for="locale in availableLocales" :key="locale.value" :value="locale.value">
        {{ locale.label }}
      </option>
    </select>
  </div>
</template>

<script setup lang="ts">
import { useLocale } from '../composables/useI18n';
import { availableLocales } from '../locales';

const { currentLocale } = useLocale();
</script> 