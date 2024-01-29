FROM node:15.8.0-alpine

WORKDIR /frontend

COPY ./package*.json /frontend

RUN npm install && \
    npm run build && \
    rm -rf node_modules && rm -rf src

COPY . /frontend
CMD ["npm", "start"]