# ใช้ base image ที่ต้องการ เช่น Python image
FROM python:3.11-slim

# ติดตั้ง dependencies ที่จำเป็น (curl, build-essential)
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && export PATH="$HOME/.cargo/bin:$PATH" \
    && rustc --version \
    && cargo --version

# เพิ่ม Cargo ใน PATH เพื่อให้สามารถเข้าถึงได้
ENV PATH="/root/.cargo/bin:${PATH}"

# ติดตั้ง dependencies ที่เกี่ยวข้องกับ Python
RUN apt-get update && apt-get install -y python3-dev

# คัดลอกไฟล์ requirements.txt ไปที่ container
COPY requirements.txt /app/requirements.txt

# กำหนด working directory
WORKDIR /app

# ติดตั้ง dependencies จาก requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# คำสั่งรันแอปพลิเคชัน
CMD ["gunicorn", "app:app"]