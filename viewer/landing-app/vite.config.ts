/**
 * The journey diagrams on the landing page — React, Tailwind and React Bits.
 *
 * Built into ../public/landing-journey/ with fixed names, so the viewer serves
 * two plain files and still has no build step at runtime:
 *
 *   npm install   (once)
 *   npm run build
 *
 * The signal engine (public/adam-journey.js) keeps the clock; this bundle only
 * draws what each card shows, from the stage and progress the engine reports.
 */
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [react(), tailwindcss()],
  define: { 'process.env.NODE_ENV': JSON.stringify('production') },
  build: {
    outDir: '../public/landing-journey',
    emptyOutDir: true,
    cssCodeSplit: false,
    sourcemap: false,
    // An app build rather than library mode: library mode leaves ES output
    // unminified whatever `minify` says, and this file is shipped as-is.
    minify: 'esbuild',
    modulePreload: false,
    rollupOptions: {
      input: 'src/main.tsx',
      // keep `mount` exported, which an app build would otherwise drop
      preserveEntrySignatures: 'exports-only',
      output: {
        format: 'es',
        entryFileNames: 'journey.js',
        assetFileNames: 'journey[extname]',
        inlineDynamicImports: true,
      },
    },
  },
});
