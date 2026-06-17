# Lightweight image — Python stdlib only, no pip install needed at runtime.
FROM python:3.12-slim

WORKDIR /app

# Copy static assets and server.
COPY index.html style.css server.py ./

EXPOSE 8000

ENV HOST=0.0.0.0 \
    PORT=8000

CMD ["python", "server.py"]
