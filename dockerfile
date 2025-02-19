FROM node
WORKDIR "/worldbricks-server"
COPY . .
RUN ng serve