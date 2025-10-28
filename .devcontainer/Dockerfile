FROM mcr.microsoft.com/vscode/devcontainers/python:3.11
RUN apt-get update && apt-get install -y poppler-utils tesseract-ocr build-essential git && apt-get clean -y
WORKDIR /workspace
COPY .. /workspace
