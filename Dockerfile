FROM node:alpine
WORKDIR /usr/src/app
COPY . /usr/src/app
RUN npm install -g @angular/cli
RUN npm install
EXPOSE 8080
CMD ["npm", "start"]
