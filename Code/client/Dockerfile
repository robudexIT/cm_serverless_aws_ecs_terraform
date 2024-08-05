FROM node:16.20.2 AS build

RUN npm install -g npm@8.19.4

WORKDIR /app 

COPY package.json ./ 
COPY package-lock.json ./

RUN npm install 


COPY . . 


RUN npm run build 


FROM nginx


COPY --from=build /app/dist/ /usr/share/nginx/html/cm_app/ 


COPY nginx.conf /etc/nginx/conf.d/default.conf


EXPOSE 80 


# CMD ["nginx", "-g", "daemon off;"]


