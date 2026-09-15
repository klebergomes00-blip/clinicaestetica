/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{html,js}",
    "./assets/**/*.{html,js}"
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        cream: '#F6F1EA',
        oat: '#E7DDD2',
        taupe: '#C9B9AA',
        chocolate: '#4A352A',
        espresso: '#241A14',
        gold: '#B08D57',
        caramel: {
          DEFAULT: '#835629',
          dark: '#6A4520',
          light: '#A16D3A',
        },
        warmWhite: '#FFFAF4',
      },
      fontFamily: {
        heading: ['Athelas', 'Cormorant Garamond', 'Playfair Display', 'Georgia', 'serif'],
        body: ['Montserrat', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'ui-monospace', 'monospace'],
      },
      screens: {
        xs: '380px',
      },
      spacing: {
        '4.5': '1.125rem',
        '18': '4.5rem',
      },
      boxShadow: {
        xs: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
      },
      opacity: {
        '6': '0.06',
        '8': '0.08',
        '12': '0.12',
        '98': '0.98',
      },
      letterSpacing: {
        cinematic: '0.32em',
        editorial: '0.22em',
        luxury: '0.14em',
      },
      animation: {
        'fade-in-up': 'fadeInUp 0.9s cubic-bezier(0.16, 1, 0.3, 1) both',
        'fade-in-down': 'fadeInDown 0.8s cubic-bezier(0.16, 1, 0.3, 1) both',
        'float-slow': 'floatSlow 7s ease-in-out infinite',
        'aurora': 'aurora 18s ease-in-out infinite alternate',
        'beam-spin': 'beamSpin 3.5s linear infinite',
        'zoom-slow': 'zoomSlow 30s linear infinite alternate',
        'pulse-subtle': 'pulseSubtle 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(24px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        fadeInDown: {
          '0%': { opacity: '0', transform: 'translateY(-14px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        floatSlow: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-8px)' },
        },
        aurora: {
          '0%': { opacity: '0.2', transform: 'scale(1) translate(0, 0)' },
          '50%': { opacity: '0.4', transform: 'scale(1.15) translate(4%, -4%)' },
          '100%': { opacity: '0.2', transform: 'scale(1) translate(-4%, 4%)' },
        },
        beamSpin: {
          to: { transform: 'rotate(360deg)' },
        },
        zoomSlow: {
          '0%': { transform: 'scale(1)' },
          '100%': { transform: 'scale(1.08)' },
        },
        pulseSubtle: {
          '0%, 100%': { opacity: '1', transform: 'scale(1)' },
          '50%': { opacity: '0.4', transform: 'scale(1.15)' },
        },
      },
    },
  },
  plugins: [],
};
