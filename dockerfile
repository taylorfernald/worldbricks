FROM node:latest
WORKDIR /worldbricks-server
COPY . .
RUN npm install
CMD [ "npm", "start" ]