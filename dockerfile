FROM node:latest
WORKDIR /worldbricks-server/src/app
RUN npm install
COPY . ./
CMD [ "npm", "start" ]