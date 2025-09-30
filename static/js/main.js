/**
 * MovieReviews - Main JavaScript
 * Interactive effects and functionality
 */

class MovieReviewsApp {
    constructor() {
        this.init();
    }

    init() {
        this.setupScrollReveal();
        this.setupSmoothScrolling();
        this.setupSearchEnhancements();
        this.setupFormValidation();
        this.setupImageLazyLoading();
        this.setupTooltips();
        this.setupParallax();
        this.setupAnimationOnScroll();
        this.setupRippleEffect();
        this.setupTypewriter();
        this.setupCounterAnimation();
        this.setupProgressBars();
        this.setupLikeSystem();
        this.setupReactionsSystem();
        this.bindEvents();
    }

    // Scroll Reveal Animation
    setupScrollReveal() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        document.querySelectorAll('.scroll-reveal, .scroll-reveal-left, .scroll-reveal-right').forEach(el => {
            observer.observe(el);
        });
    }

    // Smooth Scrolling
    setupSmoothScrolling() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    // Enhanced Search
    setupSearchEnhancements() {
        const searchInput = document.querySelector('input[name="query"]');
        if (searchInput) {
            let searchTimeout;
            
            searchInput.addEventListener('input', function() {
                clearTimeout(searchTimeout);
                const query = this.value.trim();
                
                if (query.length > 2) {
                    searchTimeout = setTimeout(() => {
                        this.classList.add('searching');
                        // Aquí podrías agregar búsqueda en tiempo real
                        setTimeout(() => {
                            this.classList.remove('searching');
                        }, 1000);
                    }, 500);
                }
            });

            // Search suggestions
            this.setupSearchSuggestions(searchInput);
        }
    }

    setupSearchSuggestions(input) {
        const suggestions = [
            'Anime', 'Películas de acción', 'Terror', 'Comedia', 'Drama',
            'Ciencia ficción', 'Marvel', 'DC', 'Studio Ghibli', 'Miyazaki'
        ];

        const suggestionContainer = document.createElement('div');
        suggestionContainer.className = 'search-suggestions';
        input.parentNode.appendChild(suggestionContainer);

        input.addEventListener('focus', () => {
            if (input.value.length === 0) {
                this.showSuggestions(suggestionContainer, suggestions.slice(0, 5), input);
            }
        });

        input.addEventListener('input', () => {
            const query = input.value.toLowerCase();
            if (query.length > 0) {
                const filtered = suggestions.filter(s => 
                    s.toLowerCase().includes(query)
                ).slice(0, 5);
                this.showSuggestions(suggestionContainer, filtered, input);
            } else {
                suggestionContainer.innerHTML = '';
            }
        });

        document.addEventListener('click', (e) => {
            if (!input.contains(e.target) && !suggestionContainer.contains(e.target)) {
                suggestionContainer.innerHTML = '';
            }
        });
    }

    showSuggestions(container, suggestions, input) {
        container.innerHTML = suggestions.map(suggestion => 
            `<div class="suggestion-item" data-suggestion="${suggestion}">${suggestion}</div>`
        ).join('');

        container.querySelectorAll('.suggestion-item').forEach(item => {
            item.addEventListener('click', () => {
                input.value = item.dataset.suggestion;
                container.innerHTML = '';
                input.focus();
            });
        });
    }

    // Form Validation
    setupFormValidation() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            const inputs = form.querySelectorAll('input, textarea, select');
            
            inputs.forEach(input => {
                input.addEventListener('blur', () => this.validateField(input));
                input.addEventListener('input', () => this.clearValidation(input));
            });

            form.addEventListener('submit', (e) => {
                let isValid = true;
                inputs.forEach(input => {
                    if (!this.validateField(input)) {
                        isValid = false;
                    }
                });

                if (!isValid) {
                    e.preventDefault();
                    this.showFormError('Por favor, corrige los errores antes de continuar.');
                }
            });
        });
    }

    validateField(field) {
        const value = field.value.trim();
        const isRequired = field.hasAttribute('required');
        let isValid = true;
        let message = '';

        // Clear previous validation
        this.clearValidation(field);

        if (isRequired && !value) {
            isValid = false;
            message = 'Este campo es obligatorio.';
        } else if (field.type === 'email' && value && !this.isValidEmail(value)) {
            isValid = false;
            message = 'Por favor, ingresa un email válido.';
        } else if (field.name === 'password1' && value && value.length < 8) {
            isValid = false;
            message = 'La contraseña debe tener al menos 8 caracteres.';
        }

        if (!isValid) {
            this.showFieldError(field, message);
        }

        return isValid;
    }

    clearValidation(field) {
        field.classList.remove('is-invalid', 'is-valid');
        const errorDiv = field.parentNode.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.remove();
        }
    }

    showFieldError(field, message) {
        field.classList.add('is-invalid');
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = message;
        field.parentNode.appendChild(errorDiv);
    }

    showFormError(message) {
        // Create or update form error message
        let errorAlert = document.querySelector('.form-error-alert');
        if (!errorAlert) {
            errorAlert = document.createElement('div');
            errorAlert.className = 'alert alert-danger form-error-alert';
            document.querySelector('form').prepend(errorAlert);
        }
        errorAlert.innerHTML = `<i class="fas fa-exclamation-circle me-2"></i>${message}`;
        errorAlert.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    // Lazy Loading for Images
    setupImageLazyLoading() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        const src = img.dataset.src || img.src;
                        
                        img.src = src;
                        img.classList.remove('lazy');
                        img.classList.add('loaded');
                        imageObserver.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('img[data-src], img.lazy').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }

    // Tooltips
    setupTooltips() {
        document.querySelectorAll('[data-tooltip]').forEach(element => {
            element.addEventListener('mouseenter', (e) => {
                this.showTooltip(e.target, e.target.dataset.tooltip);
            });

            element.addEventListener('mouseleave', () => {
                this.hideTooltip();
            });
        });
    }

    showTooltip(element, text) {
        const tooltip = document.createElement('div');
        tooltip.className = 'custom-tooltip';
        tooltip.textContent = text;
        document.body.appendChild(tooltip);

        const rect = element.getBoundingClientRect();
        tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
        tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';

        setTimeout(() => tooltip.classList.add('show'), 10);
    }

    hideTooltip() {
        const tooltip = document.querySelector('.custom-tooltip');
        if (tooltip) {
            tooltip.classList.remove('show');
            setTimeout(() => tooltip.remove(), 300);
        }
    }

    // Parallax Effect
    setupParallax() {
        const parallaxElements = document.querySelectorAll('.parallax-element');
        
        window.addEventListener('scroll', () => {
            const scrollTop = window.pageYOffset;
            
            parallaxElements.forEach(element => {
                const speed = element.dataset.speed || 0.5;
                const yPos = -(scrollTop * speed);
                element.style.transform = `translateY(${yPos}px)`;
            });
        });
    }

    // Animation on Scroll
    setupAnimationOnScroll() {
        const animatedElements = document.querySelectorAll('.animate-on-scroll');
        
        const animationObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const animationType = entry.target.dataset.animation || 'fadeInUp';
                    entry.target.classList.add(`animate-${animationType}`);
                    animationObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        animatedElements.forEach(el => animationObserver.observe(el));
    }

    // Ripple Effect
    setupRippleEffect() {
        document.querySelectorAll('.btn-ripple').forEach(button => {
            button.addEventListener('click', function(e) {
                const ripple = document.createElement('span');
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';
                ripple.classList.add('ripple');
                
                this.appendChild(ripple);
                
                setTimeout(() => ripple.remove(), 600);
            });
        });
    }

    // Typewriter Effect
    setupTypewriter() {
        document.querySelectorAll('.typewriter-text').forEach(element => {
            const text = element.textContent;
            const speed = element.dataset.speed || 100;
            
            element.textContent = '';
            element.style.borderRight = '2px solid currentColor';
            
            let i = 0;
            const typeInterval = setInterval(() => {
                element.textContent += text.charAt(i);
                i++;
                
                if (i >= text.length) {
                    clearInterval(typeInterval);
                    setTimeout(() => {
                        element.style.borderRight = 'none';
                    }, 1000);
                }
            }, speed);
        });
    }

    // Counter Animation
    setupCounterAnimation() {
        const counters = document.querySelectorAll('.counter');
        
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateCounter(entry.target);
                    counterObserver.unobserve(entry.target);
                }
            });
        });

        counters.forEach(counter => counterObserver.observe(counter));
    }

    animateCounter(element) {
        const target = parseInt(element.dataset.target);
        const duration = parseInt(element.dataset.duration) || 2000;
        const step = target / (duration / 16);
        
        let current = 0;
        const timer = setInterval(() => {
            current += step;
            element.textContent = Math.floor(current);
            
            if (current >= target) {
                element.textContent = target;
                clearInterval(timer);
            }
        }, 16);
    }

    // Progress Bars
    setupProgressBars() {
        const progressBars = document.querySelectorAll('.progress-bar-animated');
        
        const progressObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const progressBar = entry.target;
                    const targetWidth = progressBar.dataset.width || '0%';
                    
                    setTimeout(() => {
                        progressBar.style.width = targetWidth;
                    }, 200);
                    
                    progressObserver.unobserve(progressBar);
                }
            });
        });

        progressBars.forEach(bar => progressObserver.observe(bar));
    }

    // Like System
    setupLikeSystem() {
        console.log('Setting up like system...');
        const likeButtons = document.querySelectorAll('.like-btn');
        console.log('Found like buttons:', likeButtons.length);
        
        likeButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                
                if (button.disabled) {
                    this.showNotification('Inicia sesión para dar like', 'warning');
                    return;
                }
                
                const container = button.closest('.like-container');
                const postSlug = container.dataset.postSlug;
                
                if (!postSlug) {
                    console.error('Post slug not found');
                    return;
                }
                
                this.toggleLike(button, postSlug);
            });
        });
    }

    async toggleLike(button, postSlug) {
        const originalText = button.innerHTML;
        const isLiked = button.classList.contains('liked');
        
        console.log('Toggle like clicked for post:', postSlug);
        const csrfToken = this.getCSRFToken();
        console.log('CSRF Token:', csrfToken);
        console.log('CSRF Token length:', csrfToken.length);
        
        // Show loading state
        button.disabled = true;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        
        try {
            const response = await fetch(`/toggle-like/${postSlug}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
            });
            
            console.log('Response status:', response.status);
            
            const data = await response.json();
            console.log('Response data:', data);
            
            if (data.success) {
                // Update button state
                if (data.liked) {
                    button.classList.add('liked');
                    this.showNotification('¡Te gusta esta reseña!', 'success');
                } else {
                    button.classList.remove('liked');
                    this.showNotification('Ya no te gusta esta reseña', 'info');
                }
                
                // Update like count
                const likeCount = button.querySelector('.like-count');
                if (likeCount) {
                    likeCount.textContent = data.likes_count;
                }
                
                // Update like text
                const likeText = button.parentNode.querySelector('.like-text');
                if (likeText) {
                    if (data.likes_count === 0) {
                        likeText.textContent = 'Sé el primero en dar like';
                    } else if (data.likes_count === 1) {
                        likeText.textContent = 'A 1 persona le gusta';
                    } else {
                        likeText.textContent = `A ${data.likes_count} personas les gusta`;
                    }
                }
                
                // Add animation
                button.style.transform = 'scale(1.1)';
                setTimeout(() => {
                    button.style.transform = 'scale(1)';
                }, 200);
                
            } else {
                this.showNotification('Error al procesar el like', 'error');
                button.innerHTML = originalText;
            }
            
        } catch (error) {
            console.error('Error:', error);
            this.showNotification('Error de conexión', 'error');
            button.innerHTML = originalText;
        } finally {
            button.disabled = false;
        }
    }

    // Reactions System
    setupReactionsSystem() {
        console.log('Setting up reactions system...');
        const reactionContainers = document.querySelectorAll('.reactions-container');
        console.log('Found reaction containers:', reactionContainers.length);
        
        reactionContainers.forEach(container => {
            const mainBtn = container.querySelector('.reaction-main-btn');
            const panel = container.querySelector('.reactions-panel');
            const postSlug = container.dataset.postSlug;
            
            if (!mainBtn || !panel || !postSlug) return;
            
            // Toggle panel visibility
            mainBtn.addEventListener('click', (e) => {
                e.preventDefault();
                if (mainBtn.disabled) {
                    this.showNotification('Inicia sesión para reaccionar', 'warning');
                    return;
                }
                panel.classList.toggle('show');
            });
            
            // Handle reaction selection
            panel.querySelectorAll('.reaction-option').forEach(option => {
                option.addEventListener('click', (e) => {
                    e.preventDefault();
                    const reactionType = option.dataset.reaction;
                    if (reactionType) {
                        this.toggleReaction(container, postSlug, reactionType);
                        panel.classList.remove('show');
                    }
                });
            });
            
            // Close panel when clicking outside
            document.addEventListener('click', (e) => {
                if (!container.contains(e.target)) {
                    panel.classList.remove('show');
                }
            });
        });
    }

    async toggleReaction(container, postSlug, reactionType) {
        const mainBtn = container.querySelector('.reaction-main-btn');
        const originalText = mainBtn.innerHTML;
        
        console.log('Toggle reaction clicked:', postSlug, reactionType);
        
        // Show loading state
        mainBtn.disabled = true;
        mainBtn.innerHTML = '<span class="reaction-icon">⏳</span><span class="reaction-text">Cargando...</span>';
        
        try {
            const csrfToken = this.getCSRFToken();
            const formData = new FormData();
            formData.append('reaction_type', reactionType);
            formData.append('csrfmiddlewaretoken', csrfToken);
            
            const response = await fetch(`/toggle-reaction/${postSlug}/`, {
                method: 'POST',
                body: formData,
            });
            
            console.log('Response status:', response.status);
            
            const data = await response.json();
            console.log('Response data:', data);
            
            if (data.success) {
                this.updateReactionsUI(container, data);
                this.showNotification('¡Reacción actualizada!', 'success');
                
                // Add animation
                mainBtn.classList.add('animate');
                setTimeout(() => {
                    mainBtn.classList.remove('animate');
                }, 400);
                
            } else {
                this.showNotification('Error al procesar la reacción', 'error');
                mainBtn.innerHTML = originalText;
            }
            
        } catch (error) {
            console.error('Error:', error);
            this.showNotification('Error de conexión', 'error');
            mainBtn.innerHTML = originalText;
        } finally {
            mainBtn.disabled = false;
        }
    }

    updateReactionsUI(container, data) {
        const mainBtn = container.querySelector('.reaction-main-btn');
        const reactionsSummary = container.querySelector('.reactions-summary');
        
        // Update main button
        if (data.user_reaction) {
            const reactionEmojis = {
                'like': '👍',
                'love': '❤️',
                'laugh': '😂',
                'wow': '😮',
                'sad': '😢',
                'angry': '😡'
            };
            
            const reactionLabels = {
                'like': 'Me gusta',
                'love': 'Me encanta',
                'laugh': 'Me divierte',
                'wow': 'Me asombra',
                'sad': 'Me entristece',
                'angry': 'Me enoja'
            };
            
            mainBtn.classList.add('has-reaction', `reaction-${data.user_reaction}`);
            mainBtn.innerHTML = `
                <span class="reaction-icon">${reactionEmojis[data.user_reaction]}</span>
                <span class="reaction-text">${reactionLabels[data.user_reaction]}</span>
            `;
        } else {
            mainBtn.classList.remove('has-reaction', 'reaction-like', 'reaction-love', 'reaction-laugh', 'reaction-wow', 'reaction-sad', 'reaction-angry');
            mainBtn.innerHTML = `
                <span class="reaction-icon">👍</span>
                <span class="reaction-text">Reaccionar</span>
            `;
        }
        
        // Update reactions summary
        if (data.total_reactions > 0) {
            const totalCount = reactionsSummary.querySelector('.total-count');
            const countText = reactionsSummary.querySelector('.count-text');
            const breakdown = reactionsSummary.querySelector('.reactions-breakdown');
            
            if (totalCount) totalCount.textContent = data.total_reactions;
            if (countText) {
                countText.textContent = data.total_reactions === 1 ? 'reacción' : 'reacciones';
            }
            
            if (breakdown) {
                breakdown.innerHTML = '';
                Object.entries(data.reactions_by_type).forEach(([type, count]) => {
                    if (count > 0) {
                        const reactionEmojis = {
                            'like': '👍',
                            'love': '❤️',
                            'laugh': '😂',
                            'wow': '😮',
                            'sad': '😢',
                            'angry': '😡'
                        };
                        
                        const reactionDiv = document.createElement('span');
                        reactionDiv.className = `reaction-count reaction-${type}`;
                        reactionDiv.innerHTML = `
                            ${reactionEmojis[type]}
                            <span class="count">${count}</span>
                        `;
                        breakdown.appendChild(reactionDiv);
                    }
                });
            }
        } else {
            const noReactions = reactionsSummary.querySelector('.no-reactions');
            if (noReactions) {
                noReactions.innerHTML = '<span class="text-muted">Sé el primero en reaccionar</span>';
            }
        }
    }

    getCSRFToken() {
        // Try to get CSRF token from meta tag first
        const metaToken = document.querySelector('meta[name="csrf-token"]');
        if (metaToken) {
            const token = metaToken.getAttribute('content');
            if (token && token.length > 0) {
                return token;
            }
        }
        
        // Fallback to hidden input
        const inputToken = document.querySelector('[name=csrfmiddlewaretoken]');
        if (inputToken) {
            return inputToken.value;
        }
        
        console.error('CSRF token not found');
        return '';
    }

    // Event Binding
    bindEvents() {
        // Copy to clipboard
        document.querySelectorAll('.copy-button').forEach(button => {
            button.addEventListener('click', () => {
                const text = button.dataset.copy;
                navigator.clipboard.writeText(text).then(() => {
                    this.showNotification('¡Copiado al portapapeles!', 'success');
                });
            });
        });

        // Back to top
        const backToTopButton = document.querySelector('.back-to-top');
        if (backToTopButton) {
            window.addEventListener('scroll', () => {
                if (window.pageYOffset > 300) {
                    backToTopButton.classList.add('show');
                } else {
                    backToTopButton.classList.remove('show');
                }
            });

            backToTopButton.addEventListener('click', () => {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        }

        // Theme toggle (if implemented)
        const themeToggle = document.querySelector('.theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                document.body.classList.toggle('dark-theme');
                localStorage.setItem('theme', 
                    document.body.classList.contains('dark-theme') ? 'dark' : 'light'
                );
            });
        }

        // Load saved theme
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            document.body.classList.add('dark-theme');
        }
    }

    // Utility: Show Notification
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${this.getNotificationIcon(type)} me-2"></i>
            ${message}
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => notification.classList.add('show'), 100);
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    getNotificationIcon(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-circle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('MovieReviewsApp initializing...');
    new MovieReviewsApp();
    console.log('MovieReviewsApp initialized successfully');
});

// Additional CSS for JS components
const additionalStyles = `
    .searching {
        background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="45" stroke="%23667eea" stroke-width="8" fill="none" stroke-dasharray="70,200" stroke-linecap="round"><animateTransform attributeName="transform" type="rotate" values="0 50 50;360 50 50" dur="2s" repeatCount="indefinite"/></circle></svg>');
        background-repeat: no-repeat;
        background-position: right 10px center;
        background-size: 20px 20px;
    }

    .search-suggestions {
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 0 0 8px 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        max-height: 200px;
        overflow-y: auto;
    }

    .suggestion-item {
        padding: 10px 15px;
        cursor: pointer;
        transition: background-color 0.2s;
        border-bottom: 1px solid #f1f5f9;
    }

    .suggestion-item:hover {
        background-color: #f8fafc;
    }

    .suggestion-item:last-child {
        border-bottom: none;
    }

    .custom-tooltip {
        position: absolute;
        background: #1a202c;
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 14px;
        z-index: 1000;
        opacity: 0;
        transform: translateY(10px);
        transition: all 0.3s ease;
        pointer-events: none;
    }

    .custom-tooltip.show {
        opacity: 1;
        transform: translateY(0);
    }

    .custom-tooltip::after {
        content: '';
        position: absolute;
        top: 100%;
        left: 50%;
        transform: translateX(-50%);
        border: 5px solid transparent;
        border-top-color: #1a202c;
    }

    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        z-index: 1000;
        transform: translateX(400px);
        transition: transform 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    .notification.show {
        transform: translateX(0);
    }

    .notification-success { background: #10b981; }
    .notification-error { background: #ef4444; }
    .notification-warning { background: #f59e0b; }
    .notification-info { background: #3b82f6; }

    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        pointer-events: none;
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
    }

    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }

    .back-to-top {
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        background: var(--primary-color);
        color: white;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        z-index: 1000;
    }

    .back-to-top.show {
        opacity: 1;
        visibility: visible;
    }

    .back-to-top:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
`;

// Inject additional styles
const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet);