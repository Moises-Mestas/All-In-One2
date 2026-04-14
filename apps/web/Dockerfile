FROM node:20

WORKDIR /app

# 1. Copiamos como root. SonarQube es feliz porque el usuario no podrá borrar estos archivos.
COPY package*.json ./

# 2. Instalamos como root. Es ultra rápido y no congela tu PC.
RUN npm install --ignore-scripts

# 3. Copiamos el resto del código como root. Seguro e inmutable.
COPY public/ ./public/
COPY src/ ./src/
COPY index.html vite.config.ts eslint.config.js tsconfig*.json ./

# 4. TRUCO MAESTRO: Creamos la carpeta de caché de Vite y le damos permiso 
# SOLO a esa carpeta. Esto toma 0.001 segundos en vez de minutos.
RUN mkdir -p node_modules/.vite && chown -R node:node node_modules/.vite

# 5. Cambiamos al usuario seguro para la ejecución.
USER node

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]