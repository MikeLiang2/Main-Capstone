# Use an official Node.js runtime as a parent image
FROM node:22-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json first to leverage Docker cache
COPY package.json package-lock.json ./

# Install project dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port that Vite will run on in development mode
EXPOSE 5173

# Command to run the Vue.js development server
# npm run dev typically runs Vite, which binds to 0.0.0.0 by default
# Ensure your vite.config.ts is configured to listen on 0.0.0.0
CMD ["npm", "run", "dev"]
