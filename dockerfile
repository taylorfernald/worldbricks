FROM node
RUN npm install -g @angular/cli
WORKDIR "/worldbricks-server"
COPY . .
RUN ng serve