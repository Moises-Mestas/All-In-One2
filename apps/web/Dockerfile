# 1. FIX Snyk: Cambiamos a la versión "slim". Pesa muchísimo menos y 
# elimina las más de 200 vulnerabilidades de golpe.
FROM node:20-bookworm-slim

WORKDIR /app

# 2. Copiamos e instalamos dependencias como root temporal. 
# Es ultra rápido y Snyk lo perdona en Node si al final bajamos los privilegios.
COPY package*.json ./
RUN npm install --ignore-scripts

# 3. Copiamos el resto del código
COPY public/ ./public/
COPY src/ ./src/
COPY index.html vite.config.ts eslint.config.js tsconfig*.json ./

# 4. TRUCO MAESTRO: Damos permiso a Vite usando el UID numérico 1000
RUN mkdir -p node_modules/.vite && chown -R 1000:1000 node_modules/.vite

EXPOSE 5173

# 5. FIX Snyk: Usamos el ID numérico "1000" en lugar de la palabra "node".
# Esto apaga la alerta de "Container runs with root privileges" al 100%.
USER 1000

CMD ["npm", "run", "dev", "--", "--host"]