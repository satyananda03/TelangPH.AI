FROM python:3.10-slim

WORKDIR /app

# Install system dependencies untuk onnxruntime & opencv
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code first to ensure directory structure is correct
COPY . .

# Download models from Hugging Face into the correct directory
# The application code expects the models inside the 'app' folder
RUN mkdir -p app/models && \
python - <<EOF
from huggingface_hub import hf_hub_download
hf_hub_download(repo_id="Satyananda/pH_prediction",
                filename="PSPNet_liquid_segmentation.onnx",
                local_dir="app/models")
hf_hub_download(repo_id="Satyananda/pH_prediction",
                filename="ConvNeXT_pH_Classification.onnx",
                local_dir="app/models")
EOF

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]