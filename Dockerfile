FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# HuggingFace requires containers to run as a non-root user (UID 1000)
RUN useradd -m -u 1000 hfuser || echo "User exists"
USER 1000
ENV HOME=/home/hfuser \
    PATH=/home/hfuser/.local/bin:$PATH

WORKDIR $HOME/app

COPY --chown=1000:1000 requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers locally for this user to avoid permission issues
ENV PLAYWRIGHT_BROWSERS_PATH=$HOME/pw-browsers
RUN playwright install chromium

COPY --chown=1000:1000 . .

# HuggingFace expects the app to run on port 7860
EXPOSE 7860
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
