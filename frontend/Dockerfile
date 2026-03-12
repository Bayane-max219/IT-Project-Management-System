FROM node:18-alpine

WORKDIR /app

COPY package.json package-lock.json /app/
RUN npm install --legacy-peer-deps

COPY . /app/

EXPOSE 3000

ENV HOST=0.0.0.0
ENV PORT=3000

CMD ["npm", "start"]
