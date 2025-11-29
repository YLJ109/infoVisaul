document.addEventListener('DOMContentLoaded', function() {
    // 创建加载中提示元素
    function createLoadingIndicator() {
        const loading = document.createElement('div');
        loading.id = 'loading-indicator';
        loading.textContent = '加载中...';
        loading.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: #00ffff;
            font-size: 18px;
            font-weight: bold;
            font-family: "微软雅黑", sans-serif;
            text-shadow: 0 0 3px #00ffff;
            letter-spacing: 1px;
            z-index: 9999;
            background-color: rgba(0, 25, 64, 0.8);
            padding: 12px 24px;
            border-radius: 6px;
            border: 1px solid #00aaaa;
            box-shadow: 0 0 8px rgba(0, 200, 255, 0.4);
            transition: opacity 0.15s ease-out;
        `;
        document.body.appendChild(loading);
        return loading;
    }

    // 隐藏加载指示器
    function hideLoadingIndicator() {
        const loading = document.getElementById('loading-indicator');
        if (loading) {
            loading.style.opacity = '0';
            setTimeout(() => {
                if (loading.parentNode) {
                    loading.parentNode.removeChild(loading);
                }
            }, 150);
        }
    }

    // 创建加载中提示
    const loadingIndicator = createLoadingIndicator();

    // 创建随机粒子
    function createParticles() {
        // 进一步减少粒子数量以提高性能
        const particleCount = 8;
        for (let i = 0; i < particleCount; i++) {
            setTimeout(createParticle, i * 400);
        }
    }

    // 创建单个粒子
    function createParticle() {
        const particle = document.createElement('div');
        particle.className = 'particle';

        // 固定大小以提高性能
        const size = 2;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;

        // 随机初始位置
        const startX = Math.random() * 100;
        const startY = Math.random() * 100;
        particle.style.left = `${startX}%`;
        particle.style.top = `${startY}%`;

        // 固定颜色以提高性能
        particle.style.background = 'rgba(0, 255, 255, 0.6)';
        particle.style.boxShadow = '0 0 4px rgba(0, 255, 255, 0.6)';
        particle.style.willChange = 'transform, opacity';

        // 简化动画参数以提高性能
        const duration = 6;
        const xOffset = (Math.random() - 0.5) * 80;
        const yOffset = (Math.random() - 0.5) * 80;

        // 应用动画
        particle.style.animation = `floatRandom ${duration}s linear infinite`;
        particle.style.setProperty('--x-offset', `${xOffset}px`);
        particle.style.setProperty('--y-offset', `${yOffset}px`);

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
                    transform: translate(0, 0);
                    opacity: 0;
                }
                10% { opacity: 1; }
                90% { opacity: 1; }
                100% { 
                    transform: translate(var(--x-offset, 0), var(--y-offset, 0));
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

    // 定期创建新粒子以保持效果，但降低频率
    setInterval(createParticle, 1500);

    // 页面加载完成后隐藏加载指示器
    window.addEventListener('load', function() {
        // 进一步缩短延迟时间以提高响应速度
        setTimeout(hideLoadingIndicator, 150);
    });

    // 如果页面已经加载完成，立即隐藏加载指示器
    if (document.readyState === 'complete') {
        setTimeout(hideLoadingIndicator, 50);
    }
});