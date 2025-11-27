# 使用 Python 3.11 作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装必要的系统依赖
RUN apt-get update && apt-get install -y \
    libgl1-mesa-dev \
    libxcb-xinerama0 \
    libxcb-cursor0 \
    libx11-xcb1 \
    libxkbcommon-x11-0 \
    libxcb-randr0 \
    libxcb-xtest0 \
    libxcb-shape0 \
    libxcb-xfixes0 \
    libglib2.0-0 \
    libxrender1 \
    libxrandr2 \
    libxss1 \
    libgtk-3-0 \
    libgconf-2-4 \
    libasound2 \
    xvfb \
    x11vnc \
    fluxbox \
    wget \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY . .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 创建非 root 用户
RUN useradd -m -s /bin/bash dockeruser
RUN chown -R dockeruser:dockeruser /app
USER dockeruser

# 暴露端口（如果需要通过浏览器访问）
EXPOSE 5900

# 启动命令
CMD ["python", "app.py"]