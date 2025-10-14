(function() {
    // 表单元素
    const loginForm = document.getElementById('loginForm');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const togglePasswordBtn = document.getElementById('togglePassword');
    const errorMessage = document.getElementById('errorMessage');
    const usernameError = document.getElementById('usernameError');
    const passwordError = document.getElementById('passwordError');
    const loginButton = document.getElementById('loginButton');
    const rememberMeCheckbox = document.getElementById('rememberMe');
    
    // 忘记密码相关元素
    const forgotPasswordLink = document.getElementById('forgotPasswordLink');
    const forgotPasswordModal = document.getElementById('forgotPasswordModal');
    const closeForgotPassword = document.getElementById('closeForgotPassword');
    const forgotPasswordForm = document.getElementById('forgotPasswordForm');
    
    // 导航栏元素
    const navbar = document.getElementById('navbar');
    const mobileMenuBtn = document.querySelector('[class*="md:hidden"]');
    
    // 页面元素
    const loginCard = loginForm.querySelector('.bg-white');
    
    // 初始化函数
    function init() {
        // 检查本地存储中是否有保存的用户名
        checkRememberedUser();
        // 绑定事件监听器
        bindEventListeners();
        // 添加动画类
        addAnimationClasses();
    }
    
    // 检查是否有记住的用户
    function checkRememberedUser() {
        const rememberedUsername = localStorage.getItem('rememberedUsername');
        if (rememberedUsername) {
            usernameInput.value = rememberedUsername;
            rememberMeCheckbox.checked = true;
            passwordInput.focus();
        } else {
            usernameInput.focus();
        }
    }
    
    // 绑定事件监听器
    function bindEventListeners() {
        // 表单输入事件
        usernameInput.addEventListener('blur', validateUsername);
        passwordInput.addEventListener('blur', validatePassword);
        usernameInput.addEventListener('input', clearErrors);
        passwordInput.addEventListener('input', clearErrors);
        
        // 密码可见性切换
        togglePasswordBtn.addEventListener('click', togglePasswordVisibility);
        
        // 表单提交
        loginForm.addEventListener('submit', handleLoginSubmit);
        
        // 忘记密码功能
        forgotPasswordLink.addEventListener('click', openForgotPasswordModal);
        closeForgotPassword.addEventListener('click', closeForgotPasswordModal);
        forgotPasswordModal.addEventListener('click', handleModalClick);
        forgotPasswordForm.addEventListener('submit', handleForgotPasswordSubmit);
        
        // 导航栏滚动效果
        window.addEventListener('scroll', handleScroll);
        
        // 移动菜单 - 只在移动菜单按钮存在时绑定事件
        if (mobileMenuBtn) {
            mobileMenuBtn.addEventListener('click', toggleMobileMenu);
        }
        
        // 社交登录按钮
        const socialButtons = document.querySelectorAll('.grid-cols-3 button');
        socialButtons.forEach(btn => {
            btn.addEventListener('click', handleSocialLogin);
        });
    }
    
    // 添加动画类
    function addAnimationClasses() {
        // 添加页面加载动画
        document.body.classList.add('loaded');
        
        // 为登录卡片添加入场动画 - 添加存在性检查
        setTimeout(() => {
            if (loginCard && loginCard.classList) {
                loginCard.classList.add('fade-in-up');
            }
        }, 100);
    }
    
    // 验证用户名
    function validateUsername() {
        const value = usernameInput.value.trim();
        
        if (value === '') {
            showError(usernameInput, usernameError, '请输入用户名');
            return false;
        } else {
            hideError(usernameInput, usernameError);
            return true;
        }
    }
    
    // 验证密码
    function validatePassword() {
        const value = passwordInput.value;
        
        if (value === '') {
            showError(passwordInput, passwordError, '请输入密码');
            return false;
        } else if (value.length < 6) {
            showError(passwordInput, passwordError, '密码长度不能少于6位');
            return false;
        } else {
            hideError(passwordInput, passwordError);
            return true;
        }
    }
    
    // 显示错误
    function showError(input, errorElement, message) {
        input.classList.add('border-danger');
        errorElement.textContent = message;
        errorElement.classList.remove('hidden');
    }
    
    // 隐藏错误
    function hideError(input, errorElement) {
        input.classList.remove('border-danger');
        errorElement.classList.add('hidden');
    }
    
    // 清除所有错误
    function clearErrors() {
        errorMessage.classList.add('hidden');
        
        if (!usernameInput.classList.contains('focus-visible')) {
            hideError(usernameInput, usernameError);
        }
        
        if (!passwordInput.classList.contains('focus-visible')) {
            hideError(passwordInput, passwordError);
        }
    }
    
    // 切换密码可见性
    function togglePasswordVisibility() {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        
        // 切换图标
        const icon = togglePasswordBtn.querySelector('i');
        icon.classList.toggle('fa-eye');
        icon.classList.toggle('fa-eye-slash');
    }
    
    // 处理登录提交
    function handleLoginSubmit(e) {
        e.preventDefault();
        
        // 显示加载状态
        loginButton.disabled = true;
        loginButton.innerHTML = '<i class="fa fa-spinner fa-spin"></i><span>登录中...</span>';
        
        // 模拟登录请求延迟
        setTimeout(function() {
            // 验证表单
            let isValid = true;
            
            if (usernameInput.value.trim() === '') {
                usernameError.textContent = '请输入用户名';
                usernameError.classList.remove('hidden');
                usernameInput.classList.add('border-danger');
                isValid = false;
            }
            
            if (passwordInput.value.trim() === '') {
                passwordError.textContent = '请输入密码';
                passwordError.classList.remove('hidden');
                passwordInput.classList.add('border-danger');
                isValid = false;
            } else if (passwordInput.value.length < 6) {
                passwordError.textContent = '密码长度不能少于6位';
                passwordError.classList.remove('hidden');
                passwordInput.classList.add('border-danger');
                isValid = false;
            }
            
            // 如果表单验证通过，模拟登录请求
            if (isValid) {
                // 这里模拟登录失败的情况，实际应用中应替换为真实的登录API请求
                if (usernameInput.value !== 'admin' || passwordInput.value !== 'password') {
                    errorMessage.classList.remove('hidden');
                    // 添加抖动动画
                    loginForm.querySelector('div.bg-white').classList.add('animate-shake');
                    setTimeout(function() {
                        loginForm.querySelector('div.bg-white').classList.remove('animate-shake');
                    }, 500);
                } else {
                    // 登录成功，显示成功提示并跳转到主页
                    alert('登录成功！即将跳转到主页。');
                    // 实际应用中应替换为真实的跳转
                    // window.location.href = 'dashboard.html';
                }
            }
            
            // 恢复按钮状态
            loginButton.disabled = false;
            loginButton.innerHTML = '<i class="fa fa-sign-in"></i><span>登录</span>';
        }, 1500);
    }
    
    // 打开忘记密码弹窗
    function openForgotPasswordModal(e) {
        e.preventDefault();
        forgotPasswordModal.classList.remove('hidden');
        // 添加动画类
        setTimeout(function() {
            const modalContent = forgotPasswordModal.querySelector('.bg-white');
            modalContent.style.opacity = '1';
            modalContent.style.transform = 'scale(1)';
        }, 10);
    }
    
    // 关闭忘记密码弹窗
    function closeForgotPasswordModal() {
        const modalContent = forgotPasswordModal.querySelector('.bg-white');
        modalContent.style.opacity = '0';
        modalContent.style.transform = 'scale(0.95)';
        setTimeout(function() {
            forgotPasswordModal.classList.add('hidden');
        }, 300);
    }
    
    // 处理弹窗外部点击
    function handleModalClick(e) {
        if (e.target === forgotPasswordModal) {
            closeForgotPasswordModal();
        }
    }
    
    // 处理忘记密码表单提交
    function handleForgotPasswordSubmit(e) {
        e.preventDefault();
        const forgotUsername = document.getElementById('forgotUsername');
        if (forgotUsername.value.trim() === '') {
            alert('请输入用户名');
            return;
        }
        
        // 显示加载状态
        const submitBtn = this.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fa fa-spinner fa-spin mr-2"></i>发送中...';
        
        // 模拟请求延迟
        setTimeout(function() {
            alert('重置密码链接已发送到您的邮箱，请查收！');
            closeForgotPasswordModal();
            forgotPasswordForm.reset();
            submitBtn.disabled = false;
            submitBtn.textContent = '发送重置链接';
        }, 1500);
    }
    
    // 处理滚动事件
    function handleScroll() {
        if (window.scrollY > 10) {
            navbar.classList.add('py-2');
            navbar.classList.add('shadow');
            navbar.classList.remove('py-4');
            navbar.classList.remove('shadow-sm');
        } else {
            navbar.classList.add('py-4');
            navbar.classList.add('shadow-sm');
            navbar.classList.remove('py-2');
            navbar.classList.remove('shadow');
        }
    }
    
    // 切换移动菜单
    function toggleMobileMenu() {
        // 检查是否存在移动导航
        const mobileNav = document.querySelector('nav.hidden.md\\:hidden');
        if (mobileNav) {
            const isOpen = mobileNav.classList.toggle('hidden');
            
            // 切换图标
            const icon = mobileMenuBtn.querySelector('i');
            if (isOpen) {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            } else {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            }
        }
    }
    
    // 处理社交登录
    function handleSocialLogin(e) {
        const platform = e.currentTarget.querySelector('i').className;
        let platformName = '第三方平台';
        
        if (platform.includes('weixin')) platformName = '微信';
        else if (platform.includes('qq')) platformName = 'QQ';
        else if (platform.includes('weibo')) platformName = '微博';
        else if (platform.includes('music')) platformName = '抖音';
        
        alert(`即将跳转到${platformName}授权页面...`);
    }
    
    // 初始化页面
    init();
})();