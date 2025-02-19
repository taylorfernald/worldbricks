FROM node:latest
WORKDIR /worldbricks-server/src/app
COPY package.json .
RUN npm install
COPY . ./
CMD [ "npm", "start" ]