/* 页面过渡动画 */
document.addEventListener('DOMContentLoaded', function () {
  // 为封面元素添加进入动画
  setTimeout(function() {
    const coverMain = document.querySelector('.cover-main');
    if (coverMain) {
      const elements = coverMain.children;
      Array.from(elements).forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'all 0.5s ease';
        
        setTimeout(() => {
          el.style.opacity = '1';
          el.style.transform = 'translateY(0)';
        }, 300 + index * 200);
      });
    }
  }, 200);
  
  // 初始化粒子背景
  if (window.location.hash === '' || window.location.hash === '#/') {
    initParticles();
  }
  
  window.addEventListener('hashchange', function() {
    if (window.location.hash === '' || window.location.hash === '#/') {
      initParticles();
    }
  });
});

function initParticles() {
  setTimeout(function() {
    const cover = document.querySelector('section.cover');
    if (cover && !document.getElementById('particles-js')) {
      const particlesContainer = document.createElement('div');
      particlesContainer.id = 'particles-js';
      particlesContainer.style.position = 'absolute';
      particlesContainer.style.top = '0';
      particlesContainer.style.left = '0';
      particlesContainer.style.width = '100%';
      particlesContainer.style.height = '100%';
      particlesContainer.style.zIndex = '0';
      particlesContainer.style.pointerEvents = 'none';
      
      cover.style.position = 'relative';
      cover.insertBefore(particlesContainer, cover.firstChild);
      
      loadScript('https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js', function() {
        if (window.particlesJS) {
          window.particlesJS('particles-js', {
            "particles": {
              "number": {
                "value": 60,
                "density": {
                  "enable": true,
                  "value_area": 800
                }
              },
              "color": {
                "value": "#ffffff"
              },
              "shape": {
                "type": "circle",
                "stroke": {
                  "width": 0,
                  "color": "#000000"
                }
              },
              "opacity": {
                "value": 0.3,
                "random": true,
                "anim": {
                  "enable": false,
                  "speed": 1,
                  "opacity_min": 0.1,
                  "sync": false
                }
              },
              "size": {
                "value": 3,
                "random": true,
                "anim": {
                  "enable": false,
                  "speed": 40,
                  "size_min": 0.1,
                  "sync": false
                }
              },
              "line_linked": {
                "enable": true,
                "distance": 150,
                "color": "#ffffff",
                "opacity": 0.2,
                "width": 1
              },
              "move": {
                "enable": true,
                "speed": 2,
                "direction": "none",
                "random": false,
                "straight": false,
                "out_mode": "out",
                "bounce": false,
                "attract": {
                  "enable": false,
                  "rotateX": 600,
                  "rotateY": 1200
                }
              }
            },
            "interactivity": {
              "detect_on": "canvas",
              "events": {
                "onhover": {
                  "enable": true,
                  "mode": "grab"
                },
                "onclick": {
                  "enable": false,
                  "mode": "push"
                },
                "resize": true
              },
              "modes": {
                "grab": {
                  "distance": 140,
                  "line_linked": {
                    "opacity": 1
                  }
                }
              }
            },
            "retina_detect": true
          });
        }
      });
    }
  }, 500);
}

function loadScript(url, callback) {
  const script = document.createElement('script');
  script.type = 'text/javascript';
  script.src = url;
  script.onload = callback;
  document.head.appendChild(script);
}
