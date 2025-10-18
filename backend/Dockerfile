FROM python:3.11-slim

# System libs needed by trimesh/shapely on Linux
RUN apt-get update && apt-get install -y \
    libgl1 libglib2.0-0 libgeos-c1v5 libspatialindex-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
