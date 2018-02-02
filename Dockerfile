FROM node:carbon

WORKDIR /usr/src/app

COPY apiv1/package*.json ./apiv1/

RUN cd apiv1 
RUN npm install
RUN cd ..

COPY . .

CMD [ "npm", "start" ]