# ─────────────────────────────────────────────────────────────────────────────
# Stage 1 : Build React (production)
# ─────────────────────────────────────────────────────────────────────────────
FROM node:18-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install --legacy-peer-deps

COPY . .

# Build production (output → /app/build)
ENV REACT_APP_API_URL=http://localhost:8000/api
RUN npm run build

# ─────────────────────────────────────────────────────────────────────────────
# Stage 2 : Nginx pour servir la SPA React
# ─────────────────────────────────────────────────────────────────────────────
FROM nginx:1.25-alpine AS production

COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx-spa.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
