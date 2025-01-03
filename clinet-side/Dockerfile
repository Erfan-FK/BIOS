# Stage 1: Development with Vite (dev-stage)
FROM node:18 AS dev-stage

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to install dependencies
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the project files
COPY . .

# Expose Vite's default dev server port (5173)
EXPOSE 5173

# Start Vite's development server with hot-reload
CMD ["npm", "run", "dev"]

# Stage 2: Production build with NGINX (build-stage)
FROM node:18 AS build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 3: Serve with NGINX (production)
FROM nginx:stable-alpine
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
