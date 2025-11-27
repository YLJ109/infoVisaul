@echo off
echo Building Docker image for InfoVisaul...
docker build -t infovisaul .

echo.
echo Docker image built successfully!
echo.
echo To run the application, use one of the following commands:
echo.
echo Option 1 - Run directly:
echo   docker run -it --rm -e DISPLAY=host.docker.internal:0 infovisaul
echo.
echo Option 2 - Run with docker-compose:
echo   docker-compose up
echo.
pause