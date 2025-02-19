FROM node:latest
WORKDIR /worldbricks-server
COPY . .
RUN ls
RUN npm install
CMD [ "npm", "start" ]