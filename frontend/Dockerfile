# Base image
FROM node:16

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the application
COPY . .

# Build the React app
RUN npm run build

# Expose port 3000 for React
EXPOSE 3000

# Run the React app
CMD ["npm", "start"]
