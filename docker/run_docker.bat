@echo off
echo Starting InfoVisaul application in Docker container...
echo Make sure you have built the Docker image first using build_docker.bat
echo.

docker run -it --rm -e DISPLAY=host.docker.internal:0 -v %cd%/data:/app/data infovisaul

echo.
pause