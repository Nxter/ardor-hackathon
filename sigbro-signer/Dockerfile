FROM node:14.7.0-buster

WORKDIR /opt/app

COPY package*.json ./
RUN apt-get update && apt-get install git -y && rm -rf /var/lib/apt/lists/* && npm install

COPY . . 

EXPOSE 3000
CMD [ "node", "bin/www" ]