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
  const starCount = 50;
  for (let i = 0; i < starCount; i++) {
    const star = document.createElement('div');
    star.className = 'star';
    
    // 随机位置
    const left = Math.random() * 100;
    const top = Math.random() * 100;
    
    // 随机动画时间和延迟
    const duration = 2 + Math.random() * 4;
    const delay = Math.random() * 5;
    
    // 随机大小
    const size = 1 + Math.random() * 2;
    
    // 应用样式
    star.style.cssText = `
      left: ${left}%;
      top: ${top}%;
      width: ${size}px;
      height: ${size}px;
      --duration: ${duration}s;
      --delay: ${delay}s;
    `;
    
    starsContainer.appendChild(star);
  }
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
