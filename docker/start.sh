#!/bin/bash

# 启动 Xvfb 虚拟显示服务器
Xvfb :99 -screen 0 1024x768x24 &
export DISPLAY=:99

# 启动 Fluxbox 窗口管理器
fluxbox &

# 启动 VNC 服务器以便可以查看 GUI
x11vnc -display :99 -forever -shared -passwd password &

# 运行应用程序
python app.py