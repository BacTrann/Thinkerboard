# Use an official Node.js runtime as a parent image
FROM node:18-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install production dependencies
# Using --omit=dev is the modern equivalent of --production
RUN npm install --omit=dev

# Copy the rest of the application source code to the working directory
COPY . .

# Make port 5001 available to the world outside this container
EXPOSE 5001

# Define the command to run the app
CMD ["node", "src/server.js"]
