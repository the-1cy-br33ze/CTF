FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
RUN mkdir files admin-files

RUN echo "Hi! Advice of the day - if you want to hide something, you should hide it in the most visible place. Good Luck!" > /app/files/readme.md && \
    echo "flag{str@ight_fr0m_th3_2000s}" > admin-files/flag

COPY . .
EXPOSE 3001
CMD ["node", "app.js"]