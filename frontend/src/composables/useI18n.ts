import { createI18n } from 'vue-i18n'
import { ref, watch } from 'vue'
import messages from '../locales'
import type { Locale } from '../locales'

const STORAGE_KEY = 'tiny-manus-locale'

// Get current language from localStorage, default to English
const getStoredLocale = (): Locale => {
  const storedLocale = localStorage.getItem(STORAGE_KEY)
  return (storedLocale as Locale) || 'zh'
}

// Create i18n instance
export const i18n = createI18n({
  legacy: false, // Use Composition API mode
  locale: getStoredLocale(),
  fallbackLocale: 'zh',
  messages
})

// Create a composable to use in components
export function useLocale() {
  const currentLocale = ref(getStoredLocale())

  // Switch language
  const setLocale = (locale: Locale) => {
    i18n.global.locale.value = locale
    currentLocale.value = locale
    localStorage.setItem(STORAGE_KEY, locale)
    document.querySelector('html')?.setAttribute('lang', locale)
  }

  // Watch language change
  watch(currentLocale, (val) => {
    setLocale(val)
  })

  return {
    currentLocale,
    setLocale
  }
}

export default i18n 