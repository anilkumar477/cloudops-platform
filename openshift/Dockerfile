FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

# Allow arbitrary OpenShift UIDs to access application files
RUN chgrp -R 0 /app && \
    chmod -R g=u /app

EXPOSE 5000

# Test locally with a non-root user
USER 1001

CMD ["python", "app/app.py"]
