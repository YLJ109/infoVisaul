import sys
import tempfile

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMessageBox, QPushButton
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6 import QtCore
from PyQt6.QtWebEngineCore import QWebEngineSettings
import visual.setting as setting
import os

class CodeTemplate(QWidget):

    def __init__(self):
        super().__init__()
        self.web_view = None
        self.setWindowTitle("公司性质与岗位数量关联")
        # 获取当前窗口所在的屏幕
        current_screen = self.screen()  # QWidget 自带的 screen() 方法
        # 获取该屏幕的可用宽度
        current_screen_width = current_screen.availableGeometry().width()
        current_screen_height = current_screen.availableGeometry().height()

        self.win_w = current_screen_width//3-10
        self.win_h = current_screen_height//2-50
        self.web_bg_color = "#001940"  # 科技感深蓝背景

        self.data_path = setting.data_path # 数据文件路径
        self.echarts_js_path = setting.echarts_js_path # ECharts JS 文件路径
        self.china_geo_path = getattr(setting, 'china_geo_path', None) # China Geo 文件路径

        self.echarts_js_content = self._load_echarts_js()   # 读取 ECharts JS 内容
        self.init_ui() # 初始化UI
        self.load_data()    # 加载数据
        self.update_chart() # 显示初始图表

    def init_ui(self):
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        # 创建网页视图用于显示图表
        self.web_view = QWebEngineView()
        self.enlarge_chart_button = QPushButton()

        self.enlarge_chart_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                padding-left:10px;
                border: 1px solid rgb(0, 255, 255);
                margin-left:5px;
                margin-right:5px;
                
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        self.enlarge_chart_button.setIcon(QIcon("./visual/static/img/enlargement_button.png"))
        self.enlarge_chart_button.setMinimumSize(20, 20)
        self.enlarge_chart_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.enlarge_chart_button.setIconSize(QSize(16, 16))

        # 设置WebEngine的参数，解决可能的显示问题
        self.web_view.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)

        # 启用WebGL和硬件加速以支持3D图表
        self.web_view.settings().setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)

        main_layout.addWidget(self.web_view, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.enlarge_chart_button)

    def _load_echarts_js(self):
        """读取 ECharts JS 文件内容"""
        try:
            with open(self.echarts_js_path, 'r', encoding='utf-8') as f:
                echarts_content = f.read()

            # 如果有单独的地理数据文件，也加载它
            if self.china_geo_path and os.path.exists(self.china_geo_path):
                with open(self.china_geo_path, 'r', encoding='utf-8') as f:
                    geo_content = f.read()
                # 将地理数据附加到echarts内容后面
                echarts_content = echarts_content + ";\n" + geo_content

            return echarts_content
        except Exception as e:
            QMessageBox.warning(self, "警告", f"无法加载 ECharts JS 文件: {str(e)}", QMessageBox.StandardButton.Ok)
            return None

    def load_data(self):
        """加载数据"""
        pass

    def create_job_count_chart(self):
        """创建按岗位数量统计的分组柱状图"""
        pass

    def update_chart(self):
        # 只生成岗位数量统计图表
        chart = self.create_job_count_chart()

        # 检查图表是否成功创建
        if chart is None:
            # 图表创建失败
            return

        # 1. 渲染图表到临时HTML文件，使用离线模式
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8') as temp_file:
            chart.render(path=temp_file.name, template_name="simple_chart.html", echarts_js="")

        # 2. 读取临时HTML文件内容
        with open(temp_file.name, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 3. 将ECharts JS内容嵌入到HTML的<head>标签中，并设置body背景色
        head_end_index = html_content.find('</head>')
        if head_end_index != -1:
            # 在head中添加自定义CSS样式设置body背景色以及padding和margin为0
            custom_style = f'''
            <link rel="stylesheet" type="text/css" href="{os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static', 'css', 'style.css').replace(os.sep, '/')}" />
            '''
            # 添加JavaScript来创建随机粒子效果
            particle_script = f'''
            <script src="{os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static', 'js', 'visual.js').replace(os.sep, '/')}"></script>
            '''

            modified_html = (html_content[:head_end_index] + f'<script>{self.echarts_js_content}</script>' + custom_style
                             + particle_script + html_content[head_end_index:])

        else:
            # 如果没有</head>标签，就加在<body>前面
            body_start_index = html_content.find('<body>')
            custom_style = f'''
            <link rel="stylesheet" type="text/css" href="{os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static', 'css', 'style.css').replace(os.sep, '/')}" />
            '''
            # 添加JavaScript来创建随机粒子效果
            particle_script = '''
            <script>
            document.addEventListener('DOMContentLoaded', function() {
                // 创建随机粒子
                function createParticles() {
                    const particleCount = 40;
                    for (let i = 0; i < particleCount; i++) {
                        setTimeout(createParticle, i * 300); // 每300毫秒创建一个粒子
                    }
                }
                
                // 创建单个粒子
                function createParticle() {
                    const particle = document.createElement('div');
                    particle.className = 'particle';
                    
                    // 随机大小 (1px 到 4px)
                    const size = Math.random() * 3 + 1;
                    particle.style.width = `${size}px`;
                    particle.style.height = `${size}px`;
                    
                    // 随机初始位置
                    const startX = Math.random() * 100;
                    const startY = Math.random() * 100;
                    particle.style.left = `${startX}%`;
                    particle.style.top = `${startY}%`;
                    
                    // 随机颜色
                    const colors = [
                        'rgba(0, 255, 255, 0.8)',   // 青色
                        'rgba(0, 200, 255, 0.6)',   // 蓝青色
                        'rgba(0, 150, 255, 0.5)'    // 蓝色
                    ];
                    const color = colors[Math.floor(Math.random() * colors.length)];
                    particle.style.background = color;
                    particle.style.boxShadow = `0 0 ${size * 2}px ${color}`;
                    
                    // 随机动画参数
                    const duration = Math.random() * 20 + 10; // 10-30秒
                    const xOffset = (Math.random() - 0.5) * 200; // -100px 到 100px
                    const yOffset = (Math.random() - 0.5) * 200; // -100px 到 100px
                    const rotation = Math.random() * 360; // 0-360度
                    
                    // 应用动画
                    particle.style.animation = `floatRandom ${duration}s linear infinite`;
                    particle.style.setProperty('--x-offset', `${xOffset}px`);
                    particle.style.setProperty('--y-offset', `${yOffset}px`);
                    particle.style.setProperty('--rotation', `${rotation}deg`);
                    
                    document.body.appendChild(particle);
                    
                    // 粒子生命周期结束后移除
                    setTimeout(() => {
                        if (particle.parentNode) {
                            particle.parentNode.removeChild(particle);
                        }
                    }, duration * 1000);
                }
                
                // 添加粒子动画关键帧
                function addParticleAnimation() {
                    const style = document.createElement('style');
                    style.innerHTML = `
                        @keyframes floatRandom {
                            0% { 
                                transform: translate(0, 0) rotate(0deg);
                                opacity: 0;
                            }
                            10% { opacity: 1; }
                            90% { opacity: 1; }
                            100% { 
                                transform: translate(var(--x-offset, 0), var(--y-offset, 0)) rotate(var(--rotation, 360deg));
                                opacity: 0;
                            }
                        }
                    `;
                    document.head.appendChild(style);
                }
                
                // 初始化粒子动画
                addParticleAnimation();
                
                // 初始化粒子
                createParticles();
                
                // 定期创建新粒子以保持效果
                setInterval(createParticle, 800);
            });
            </script>
            '''
            modified_html = (html_content[:body_start_index] + f'<script>{self.echarts_js_content}</script>' + custom_style
                             + particle_script + html_content[body_start_index:])
                             
        # 4. 在WebView中显示修改后的HTML
        self.web_view.setHtml(modified_html, baseUrl=QtCore.QUrl.fromLocalFile(temp_file.name))
        # 5. 删除临时文件
        os.unlink(temp_file.name)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CodeTemplate()
    window.show()
    sys.exit(app.exec())