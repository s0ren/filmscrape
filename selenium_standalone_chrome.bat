rem Note: Only one Standalone container can run on port 4444 at the same time.
docker run -d -p 4444:4444 --shm-size="2g" selenium/standalone-chrome:4.27.0-20241204
