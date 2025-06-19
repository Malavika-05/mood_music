# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy files into container
COPY . .

# Install dependencies
RUN python3 -m pip install --no-cache-dir --break-system-packages -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python3", "app.py"]
