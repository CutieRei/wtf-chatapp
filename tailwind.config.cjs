const colors = require("tailwindcss/colors");

/** @type {import('tailwindcss').Config} */ 
module.exports = {
  darkMode: "class",
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        primary: colors.violet[900],
        secondary: colors.violet[600],
        neutral: colors.violet[200]
      }
    }
  },
  plugins: [
    require("tailwind-scrollbar")
  ]
};