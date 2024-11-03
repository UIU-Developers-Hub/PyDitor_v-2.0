/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        editor: {
          bg: '#1e1e1e',
          text: '#d4d4d4',
          line: '#858585'
        },
        terminal: {
          bg: '#1a1a1a',
          text: '#ffffff'
        }
      }
    },
  },
  plugins: [],
}