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