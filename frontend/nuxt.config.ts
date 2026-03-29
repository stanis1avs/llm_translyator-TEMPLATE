export default defineNuxtConfig({
  ssr: false,

  modules: ['vuetify-nuxt-module', '@pinia/nuxt'],

  vuetify: {
    vuetifyOptions: {
      theme: {
        defaultTheme: 'dark',
        themes: {
          dark: {
            colors: {
              primary: '#7C4DFF',
              secondary: '#448AFF',
              surface: '#1E1E2E',
              background: '#13131F',
            },
          },
        },
      },
    },
  },

  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:8000',
      wsBase: 'ws://localhost:8000',
    },
  },

  compatibilityDate: '2024-11-01',
})
