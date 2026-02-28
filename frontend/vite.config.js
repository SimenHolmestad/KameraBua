import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig(({ command }) => ({
  base: command === "serve" ? "/" : "/static/react/",
  plugins: [react()],
  build: {
    outDir: "build",
    emptyOutDir: true,
  },
  server: {
    host: true,
    port: 5000,
    open: `http://localhost:5000/`,
    proxy: {
      "/albums": `http://localhost:3000`,
      "/qr_codes": `http://localhost:3000`,
      "/static": `http://localhost:3000`,
    },
  },
}));
