// 生成闪烁的星星
document.addEventListener('DOMContentLoaded', function() {
  // 等待DOM加载完成后添加星星
  setTimeout(function() {
    const cover = document.querySelector('section.cover');
    if (cover) {
      addStars(cover);
      enhanceQuote();
    }
  }, 300);
  
  // 当hash改变时检查是否需要添加星星
  window.addEventListener('hashchange', function() {
    setTimeout(function() {
      const cover = document.querySelector('section.cover');
      if (cover && !cover.querySelector('.stars')) {
        addStars(cover);
        enhanceQuote();
      }
    }, 300);
  });
});

// 添加星星到封面
function addStars(cover) {
  // 创建星星容器
  const starsContainer = document.createElement('div');
  starsContainer.className = 'stars';
  cover.appendChild(starsContainer);
  
  // 添加多个星星
  const starCount = 60;
  
  // 定义几种星星颜色
  const starColors = [
    '#FFD700', // 金色
    '#00BFFF', // 亮蓝色
    '#FF69B4', // 亮粉色
    '#7FFFD4', // 碧绿色
    '#9370DB', // 中紫色
    '#FF6347'  // 番茄红
  ];
  
  for (let i = 0; i < starCount; i++) {
    const star = document.createElement('div');
    star.className = 'star';
    
    // 随机位置
    const left = Math.random() * 100;
    const top = Math.random() * 100;
    
    // 随机动画时间和延迟
    const duration = 2 + Math.random() * 4;
    const delay = Math.random() * 5;
    
    // 随机大小 - 增大尺寸
    const size = 3 + Math.random() * 4;
    
    // 随机颜色
    const colorIndex = Math.floor(Math.random() * starColors.length);
    const starColor = starColors[colorIndex];
    
    // 随机透明度 - 更明显
    const opacity = 0.7 + Math.random() * 0.3;
    
    // 应用样式
    star.style.cssText = `
      left: ${left}%;
      top: ${top}%;
      width: ${size}px;
      height: ${size}px;
      --duration: ${duration}s;
      --delay: ${delay}s;
      --star-color: ${starColor};
      --star-opacity: ${opacity};
    `;
    
    starsContainer.appendChild(star);
  }
  
  // 添加一些特大的星星
  addSpecialStars(starsContainer);
}

// 增强引言效果
function enhanceQuote() {
  const quote = document.querySelector('section.cover blockquote');
  if (quote) {
    // 添加文字分割效果
    const quoteText = quote.querySelector('p');
    if (quoteText) {
      const text = quoteText.innerHTML;
      const words = text.split('·');
      
      if (words.length === 3) {
        const coloredText = `
          <span class="quote-part" style="color: #f6d365;">${words[0].trim()}</span>
          <span class="quote-separator">·</span>
          <span class="quote-part" style="color: #fd6585;">${words[1].trim()}</span>
          <span class="quote-separator">·</span>
          <span class="quote-part" style="color: #feb47b;">${words[2].trim()}</span>
        `;
        quoteText.innerHTML = coloredText;
      }
    }
  }
}

// 添加一些特殊的大星星
function addSpecialStars(container) {
  // 添加5个特大星星
  for (let i = 0; i < 5; i++) {
    const specialStar = document.createElement('div');
    specialStar.className = 'star special-star';
    
    // 随机位置
    const left = 10 + Math.random() * 80; // 避免太靠近边缘
    const top = 10 + Math.random() * 80;
    
    // 随机动画时间和延迟
    const duration = 4 + Math.random() * 3;
    const delay = Math.random() * 2;
    
    // 大尺寸
    const size = 8 + Math.random() * 5;
    
    // 亮丽的颜色
    const hue = Math.floor(Math.random() * 360);
    const saturation = 80 + Math.floor(Math.random() * 20);
    const lightness = 60 + Math.floor(Math.random() * 20);
    const starColor = `hsl(${hue}, ${saturation}%, ${lightness}%)`;
    
    // 应用样式
    specialStar.style.cssText = `
      left: ${left}%;
      top: ${top}%;
      width: ${size}px;
      height: ${size}px;
      --duration: ${duration}s;
      --delay: ${delay}s;
      --star-color: ${starColor};
      --star-opacity: 0.9;
      filter: blur(0.5px);
      z-index: 2;
    `;
    
    // 添加光芒效果
    addStarRays(specialStar);
    
    container.appendChild(specialStar);
  }
}

// 为星星添加光芒
function addStarRays(star) {
  // 创建父容器
  const raysContainer = document.createElement('div');
  raysContainer.className = 'star-rays';
  raysContainer.style.cssText = `
    position: absolute;
    top: 50%;
    left: 50%;
    width: 200%;
    height: 200%;
    transform: translate(-50%, -50%);
  `;
  
  star.appendChild(raysContainer);
  
  // 创建4-8条光芒
  const rayCount = 4 + Math.floor(Math.random() * 5);
  const starColor = star.style.getPropertyValue('--star-color');
  
  for (let i = 0; i < rayCount; i++) {
    const ray = document.createElement('div');
    ray.className = 'star-ray';
    
    // 计算角度
    const angle = (i / rayCount) * 360;
    const length = 100 + Math.random() * 100; // 光芒长度
    
    ray.style.cssText = `
      position: absolute;
      top: 50%;
      left: 50%;
      width: ${length}%;
      height: 1px;
      background: linear-gradient(90deg, ${starColor} 0%, rgba(255,255,255,0) 100%);
      transform: translate(-50%, -50%) rotate(${angle}deg);
      opacity: 0.6;
      animation: rayPulse 4s ease-in-out infinite;
      animation-delay: ${Math.random() * 2}s;
    `;
    
    raysContainer.appendChild(ray);
  }
}

// 在文档中添加新的动画
document.addEventListener('DOMContentLoaded', function() {
  const styleSheet = document.createElement('style');
  styleSheet.textContent = `
    @keyframes rayPulse {
      0%, 100% {
        opacity: 0.2;
        transform: translate(-50%, -50%) rotate(var(--angle)) scale(0.8);
      }
      50% {
        opacity: 0.7;
        transform: translate(-50%, -50%) rotate(var(--angle)) scale(1.2);
      }
    }
    
    .special-star {
      animation: specialTwinkle var(--duration) ease-in-out infinite var(--delay);
    }
    
    @keyframes specialTwinkle {
      0%, 100% {
        opacity: 0.3;
        transform: scale(0.8) rotate(0deg);
      }
      50% {
        opacity: var(--star-opacity);
        transform: scale(1.2) rotate(45deg);
      }
    }
  `;
  document.head.appendChild(styleSheet);
});
