class Shop {
    constructor() {
        this.products = products.items;
        this.sessionId = Date.now().toString();
        this.init();
    }
    
    init() {
        this.loadState();
        this.render();
        this.bindEvents();
        
        // Проверяем, есть ли переданный баланс из Python
        this.checkForInitialBalance();
    }
    
    // Проверяем, передал ли Python начальный баланс
    checkForInitialBalance() {
        const urlParams = new URLSearchParams(window.location.search);
        const initialBalance = urlParams.get('initial_balance');
        
        if (initialBalance) {
            const balance = parseInt(initialBalance);
            if (!isNaN(balance) && balance > 0) {
                this.balance = balance;
                this.saveState();
                this.showMessage(`Начальный баланс установлен: ${balance.toLocaleString()} ${TEXTS.currency}`, 'success');
                this.updateDisplay();
            }
        }
    }
    
    loadState() {
        // Пытаемся получить баланс из Python данных или localStorage
        const pythonData = localStorage.getItem('python_initial_balance');
        if (pythonData) {
            try {
                const data = JSON.parse(pythonData);
                if (data.balance && data.timestamp) {
                    // Используем баланс из Python если он был установлен менее 5 минут назад
                    const fiveMinutesAgo = Date.now() - 5 * 60 * 1000;
                    if (data.timestamp > fiveMinutesAgo) {
                        this.balance = data.balance;
                        localStorage.removeItem('python_initial_balance'); // Очищаем после использования
                        console.log(`Использован баланс из Python: ${this.balance}`);
                    }
                }
            } catch (e) {
                console.error('Ошибка чтения Python баланса:', e);
            }
        }
        
        // Если не установлен через Python, используем localStorage или значение по умолчанию
        if (typeof this.balance === 'undefined') {
            const savedBalance = localStorage.getItem('shop_balance');
            this.balance = savedBalance ? parseInt(savedBalance) : 30000;
        }
        
        // Загружаем корзину
        const savedCart = localStorage.getItem('shop_cart');
        this.cart = savedCart ? JSON.parse(savedCart) : [];
    }
    
    saveState() {
        localStorage.setItem('shop_balance', this.balance);
        localStorage.setItem('shop_cart', JSON.stringify(this.cart));
    }
    
    showMessage(text, type = 'success') {
        // Удаляем старые сообщения
        document.querySelectorAll('.message').forEach(msg => msg.remove());
        
        const message = document.createElement('div');
        message.className = `message ${type}`;
        message.textContent = text;
        message.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 25px;
            border-radius: 10px;
            color: white;
            background: ${type === 'success' ? '#00b09b' : '#ff4757'};
            z-index: 1001;
            animation: slideInRight 0.3s ease;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        `;
        
        document.body.appendChild(message);
        
        setTimeout(() => {
            if (message.parentNode) {
                message.style.animation = 'slideInRight 0.3s ease reverse';
                setTimeout(() => message.remove(), 300);
            }
        }, 3000);
    }
    
    showModal(title, message, buttons = [], options = {}) {
        // Удаляем старые модальные окна
        document.querySelectorAll('.modal-overlay').forEach(modal => modal.remove());
        
        const overlay = document.createElement('div');
        overlay.className = 'modal-overlay';
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.7);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 2000;
            animation: fadeIn 0.3s ease;
        `;
        
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.style.cssText = `
            background: white;
            padding: 40px;
            border-radius: 20px;
            max-width: 500px;
            width: 90%;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            animation: slideUp 0.3s ease;
        `;
        
        // Иконка в зависимости от типа
        let icon = '✅';
        if (options.type === 'warning') icon = '⚠️';
        if (options.type === 'error') icon = '❌';
        if (options.type === 'info') icon = 'ℹ️';
        if (options.type === 'question') icon = '❓';
        
        modal.innerHTML = `
            <div style="font-size: 60px; margin-bottom: 20px;">${icon}</div>
            <h2 style="color: #333; margin-bottom: 15px; font-size: 24px;">${title}</h2>
            <p style="color: #666; margin-bottom: 25px; font-size: 16px; line-height: 1.5;">${message}</p>
            <div style="display: flex; gap: 15px; justify-content: center;">
                ${buttons.map(btn => `
                    <button class="modal-btn ${btn.class || ''}" 
                            data-action="${btn.action}" 
                            style="padding: 12px 25px; background: ${btn.color || '#667eea'}; 
                                   color: white; border: none; border-radius: 8px; 
                                   cursor: pointer; font-weight: 600; transition: all 0.3s;">
                        ${btn.text}
                    </button>
                `).join('')}
            </div>
        `;
        
        overlay.appendChild(modal);
        document.body.appendChild(overlay);
        
        // Добавляем стили анимации
        const style = document.createElement('style');
        style.textContent = `
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            @keyframes slideUp {
                from { transform: translateY(30px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            .modal-btn:hover {
                transform: scale(1.05);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
        `;
        document.head.appendChild(style);
        
        // Возвращаем промис для обработки действий
        return new Promise((resolve) => {
            modal.querySelectorAll('.modal-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    const action = btn.dataset.action;
                    overlay.remove();
                    style.remove();
                    resolve(action);
                });
            });
            
            // Закрытие по клику на оверлей
            overlay.addEventListener('click', (e) => {
                if (e.target === overlay) {
                    overlay.remove();
                    style.remove();
                    resolve('cancel');
                }
            });
        });
    }
    
    calculateTotal() {
        return this.cart.reduce((total, item) => total + item.price, 0);
    }
    
    addToCart(product) {
        if (this.balance >= product.price) {
            this.cart.push({
                ...product,
                id: Date.now(),
                addedAt: new Date().toISOString()
            });
            this.balance -= product.price;
            this.saveState();
            this.showMessage(`${TEXTS.addedToCart} ${product.showName}`, 'success');
            this.updateDisplay();
        } else {
            this.showMessage(TEXTS.lowBalanceError, 'error');
        }
    }
    
    removeFromCart(itemId, price) {
        this.cart = this.cart.filter(item => item.id !== itemId);
        this.balance += price;
        this.saveState();
        this.showMessage(TEXTS.removedFromCart, 'success');
        this.updateDisplay();
    }
    
    clearCart() {
        if (this.cart.length === 0) {
            this.showMessage(TEXTS.emptyCart, 'info');
            return;
        }
        
        const total = this.calculateTotal();
        
        this.showModal(
            TEXTS.clearCartTitle,
            `${TEXTS.clearCartMessage}<br><br><strong>${TEXTS.restoreBalance} ${total.toLocaleString()} ${TEXTS.currency}</strong>`,
            [
                {
                    text: TEXTS.clearCartConfirm,
                    action: 'confirm',
                    color: '#ff4757'
                },
                {
                    text: TEXTS.clearCartCancel,
                    action: 'cancel',
                    color: '#667eea'
                }
            ],
            { type: 'question' }
        ).then(action => {
            if (action === 'confirm') {
                // Возвращаем деньги за все товары
                this.balance += total;
                this.cart = [];
                this.saveState();
                this.showMessage(TEXTS.cartCleared, 'success');
                this.updateDisplay();
            }
        });
    }
    
    performExit() {
        // Очищаем данные сессии
        localStorage.removeItem('python_purchase_data');
        document.body.removeAttribute('data-purchase-ready');
        
        this.showMessage(TEXTS.successExit, 'success');
        
        // Устанавливаем флаг выхода в localStorage для Python скрипта
        localStorage.setItem('shop_exit_requested', JSON.stringify({
            sessionId: this.sessionId,
            timestamp: new Date().toISOString(),
            cartCleared: this.cart.length === 0,
            finalBalance: this.balance
        }));
        
        // Не отправляем сообщение окну-родителю сразу
        // Вместо этого ждем, пока окно действительно закроется
        
        // Закрываем окно через 500мс (даем время показать сообщение)
        setTimeout(() => {
            // Проверяем, было ли окно открыто через window.open
            if (window.opener) {
                // Отправляем сообщение только когда окно действительно закрывается
                window.addEventListener('beforeunload', () => {
                    window.opener.postMessage({ 
                        type: 'shop_exit',
                        sessionId: this.sessionId,
                        timestamp: new Date().toISOString()
                    }, '*');
                });
            }
            
            // Закрываем окно
            window.close();
            
            // Если окно не закрылось (например, было открыто не через window.open)
            if (!window.closed) {
                // Показываем сообщение о ручном закрытии через 1 секунду
                setTimeout(() => {
                    this.showModal(
                        TEXTS.exitTitle,
                        "Магазин готов к закрытию. Вы можете закрыть это окно вручную.",
                        [{
                            text: "Закрыть окно",
                            action: "close",
                            color: "#667eea"
                        }],
                        { type: 'info' }
                    ).then(action => {
                        if (action === 'close') {
                            // Очищаем флаги перед ручным закрытием
                            localStorage.removeItem('shop_exit_requested');
                        }
                    });
                }, 1000);
            }
        }, 500);
    }
    
    // Обновляем метод exitShop для лучшего контроля
    exitShop() {
        if (this.cart.length > 0) {
            this.showModal(
                TEXTS.exitWithCartTitle,
                `${TEXTS.exitWithCartMessage}<br><br>${TEXTS.total} ${this.calculateTotal().toLocaleString()} ${TEXTS.currency}`,
                [
                    {
                        text: TEXTS.exitWithCartConfirm,
                        action: 'clear_and_exit',
                        color: '#ff4757'
                    },
                    {
                        text: TEXTS.clearCartConfirm,
                        action: 'clear_only',
                        color: '#ffa502'
                    },
                    {
                        text: TEXTS.exitCancel,
                        action: 'cancel',
                        color: '#667eea'
                    }
                ],
                { type: 'warning' }
            ).then(action => {
                if (action === 'clear_and_exit') {
                    // Очищаем корзину и выходим
                    const total = this.calculateTotal();
                    this.balance += total;
                    this.cart = [];
                    this.saveState();
                    this.performExit();
                } else if (action === 'clear_only') {
                    // Только очищаем корзину
                    const total = this.calculateTotal();
                    this.balance += total;
                    this.cart = [];
                    this.saveState();
                    this.showMessage(TEXTS.cartCleared, 'success');
                    this.updateDisplay();
                    
                    // После очистки показываем окно выхода
                    setTimeout(() => this.confirmExit(), 500);
                }
            });
        } else {
            this.confirmExit();
        }
    }
    
    confirmExit() {
        this.showModal(
            TEXTS.exitTitle,
            TEXTS.exitMessage,
            [
                {
                    text: TEXTS.exitConfirm,
                    action: 'exit',
                    color: '#667eea'
                },
                {
                    text: TEXTS.exitCancel,
                    action: 'cancel',
                    color: '#ccc'
                }
            ],
            { type: 'info' }
        ).then(action => {
            if (action === 'exit') {
                this.performExit();
            }
        });
    }
    
    prepareForPythonProcessing() {
        if (this.cart.length === 0) {
            this.showMessage(TEXTS.emptyCartError, 'error');
            return false;
        }
        
        const purchaseData = {
            sessionId: this.sessionId,
            initialBalance: this.balance + this.calculateTotal(), // Баланс до покупки
            currentBalance: this.balance,
            cart: this.cart.map(item => ({
                programName: item.programName,
                price: item.price,
                showName: item.showName,
                addedAt: item.addedAt
            })),
            total: this.calculateTotal(),
            timestamp: new Date().toISOString(),
            status: 'pending'
        };
        
        // Сохраняем данные для Python
        localStorage.setItem('python_purchase_data', JSON.stringify(purchaseData));
        
        // Устанавливаем флаг готовности
        document.body.setAttribute('data-purchase-ready', 'true');
        
        return true;
    }
    
    checkout() {
        if (this.cart.length === 0) {
            this.showMessage(TEXTS.emptyCartError, 'error');
            return;
        }
        
        // Подготавливаем данные для Python
        if (!this.prepareForPythonProcessing()) {
            return;
        }
        
        // Показываем модальное окно
        this.modal = this.showModal(
            TEXTS.modalTitle,
            TEXTS.modalMessage,
            [
                {
                    text: TEXTS.modalCancel,
                    action: 'cancel',
                    color: '#ff4757'
                }
            ],
            { type: 'info' }
        ).then(action => {
            if (action === 'cancel') {
                this.cancelPurchase();
            }
        });
        
        // Начинаем отслеживать обработку
        this.startProcessingMonitor();
        
        this.showMessage(TEXTS.dataReadyForPython, 'success');
    }
    
    startProcessingMonitor() {
        // Проверяем статус обработки каждые 500мс
        this.processingInterval = setInterval(() => {
            const purchaseData = localStorage.getItem('python_purchase_data');
            
            if (!purchaseData) {
                // Данные удалены - обработка завершена
                this.completePurchase();
                return;
            }
            
            try {
                const data = JSON.parse(purchaseData);
                if (data.status === 'processing') {
                    // Python начал обработку
                    this.showMessage(TEXTS.statusProcessing, 'success');
                } else if (data.status === 'completed') {
                    // Python завершил обработку
                    this.completePurchase();
                } else if (data.status === 'error') {
                    // Ошибка при обработке
                    this.handleProcessingError(data.error || TEXTS.errorGeneral);
                }
            } catch (e) {
                console.error('Ошибка мониторинга:', e);
            }
        }, 500);
        
        // Таймаут на случай, если Python не ответит
        this.processingTimeout = setTimeout(() => {
            if (this.processingInterval) {
                this.handleProcessingError(TEXTS.errorBrowserClosed);
            }
        }, 300000); // 5 минут
    }
    
    completePurchase() {
        this.stopProcessingMonitor();
        
        // Очищаем корзину
        const purchaseHistory = JSON.parse(localStorage.getItem('purchase_history') || '[]');
        const currentPurchase = {
            items: this.cart,
            total: this.calculateTotal(),
            timestamp: new Date().toISOString(),
            sessionId: this.sessionId
        };
        purchaseHistory.push(currentPurchase);
        localStorage.setItem('purchase_history', JSON.stringify(purchaseHistory));
        
        this.cart = [];
        this.saveState();
        
        // Обновляем отображение
        this.updateDisplay();
        
        // Закрываем модальное окно
        if (this.modal) {
            setTimeout(() => {
                this.modal = null;
                this.showMessage(TEXTS.successPurchaseComplete, 'success');
            }, 1000);
        }
        
        // Очищаем Python данные
        localStorage.removeItem('python_purchase_data');
        document.body.removeAttribute('data-purchase-ready');
    }
    
    cancelPurchase() {
        this.stopProcessingMonitor();
        
        // Очищаем Python данные
        localStorage.removeItem('python_purchase_data');
        document.body.removeAttribute('data-purchase-ready');
        
        this.showMessage(TEXTS.purchaseCancelled, 'error');
    }
    
    handleProcessingError(error) {
        this.stopProcessingMonitor();
        
        if (this.modal) {
            this.modal = null;
        }
        
        this.showMessage(`${TEXTS.statusError}: ${error}`, 'error');
        
        // Восстанавливаем баланс (возвращаем товары в "виртуальную корзину")
        const purchaseData = localStorage.getItem('python_purchase_data');
        if (purchaseData) {
            try {
                const data = JSON.parse(purchaseData);
                if (data.cart) {
                    // Восстанавливаем баланс
                    this.balance = data.initialBalance;
                    this.saveState();
                    this.updateDisplay();
                }
            } catch (e) {
                console.error('Ошибка восстановления:', e);
            }
        }
        
        localStorage.removeItem('python_purchase_data');
        document.body.removeAttribute('data-purchase-ready');
    }
    
    stopProcessingMonitor() {
        if (this.processingInterval) {
            clearInterval(this.processingInterval);
            this.processingInterval = null;
        }
        if (this.processingTimeout) {
            clearTimeout(this.processingTimeout);
            this.processingTimeout = null;
        }
    }
    
    render() {
        const app = document.getElementById('app');
        app.innerHTML = '';
        
        const container = document.createElement('div');
        container.className = 'container';
        
        container.innerHTML = `
            <header>
                <h1>${TEXTS.shopTitle}</h1>
                <div class="balance">${TEXTS.balance} <span class="balance-amount">${this.balance.toLocaleString()}</span> ${TEXTS.currency}</div>
                <div class="session-info">${TEXTS.sessionId} ${this.sessionId.slice(-8)}</div>
            </header>
            
            <div class="content">
                <section class="products-section">
                    <h2>${TEXTS.productsTitle}</h2>
                    <div class="product-list">
                        ${this.products.map((product, index) => `
                            <div class="product-card" title="${TEXTS.hintAddToCart}">
                                <h3 class="product-name">${product.showName}</h3>
                                <div class="product-price">${product.price.toLocaleString()} ${TEXTS.currency}</div>
                                <button class="buy-button" data-index="${index}" 
                                        ${this.balance < product.price ? 'disabled' : ''}>
                                    ${this.balance >= product.price ? TEXTS.addToCart : TEXTS.insufficientFunds}
                                </button>
                            </div>
                        `).join('')}
                    </div>
                </section>
                
                <section class="cart-section">
                    <div class="cart-header">
                        <h2>${TEXTS.cartTitle} (<span class="cart-count">${this.cart.length}</span> ${TEXTS.itemsCount})</h2>
                        ${this.cart.length > 0 ? `
                            <button class="clear-cart-btn" title="${TEXTS.hintClearCart}">
                                ${TEXTS.clearCart}
                            </button>
                        ` : ''}
                    </div>
                    
                    <div class="cart-items">
                        ${this.cart.length === 0 ? 
                            `<div class="empty-cart">${TEXTS.emptyCart}</div>` : 
                            this.cart.map(item => `
                                <div class="cart-item" data-id="${item.id}">
                                    <div>
                                        <div class="product-name">${item.showName}</div>
                                        <div class="product-price">${item.price.toLocaleString()} ${TEXTS.currency}</div>
                                    </div>
                                    <button class="remove-button" data-id="${item.id}" data-price="${item.price}">
                                        ${TEXTS.remove}
                                    </button>
                                </div>
                            `).join('')
                        }
                    </div>
                    
                    ${this.cart.length > 0 ? `
                        <div class="cart-summary">
                            <div class="summary-row">
                                <span>${TEXTS.totalAmount}</span>
                                <span class="total-amount">${this.calculateTotal().toLocaleString()} ${TEXTS.currency}</span>
                            </div>
                            <div class="summary-row">
                                <span>${TEXTS.availableBalance}:</span>
                                <span class="balance-amount">${this.balance.toLocaleString()} ${TEXTS.currency}</span>
                            </div>
                            <div class="cart-actions">
                                <button class="checkout-button" title="${TEXTS.hintCheckout}">
                                    ${TEXTS.checkout}
                                </button>
                            </div>
                        </div>
                    ` : ''}
                    
                    <div class="shop-controls">
                        <h3>${TEXTS.sessionManagement}</h3>
                        <div class="control-buttons">
                            <button class="exit-btn" title="${TEXTS.hintExit}">
                                ${TEXTS.exitShop}
                            </button>
                        </div>
                    </div>
                </section>
            </div>
        `;
        
        app.appendChild(container);
        this.applyStyles();
    }
    
    applyStyles() {
        // Убедимся, что стили применены
        if (!document.querySelector('#shop-styles')) {
            const style = document.createElement('style');
            style.id = 'shop-styles';
            style.textContent = `
                .container {
                    background: white;
                    border-radius: 20px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    width: 100%;
                    max-width: 1200px;
                    overflow: hidden;
                    margin: 20px;
                    animation: slideIn 0.5s ease-out;
                }
                
                @keyframes slideIn {
                    from { opacity: 0; transform: translateY(20px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                
                @keyframes slideInRight {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
                
                header {
                    background: linear-gradient(90deg, #667eea, #764ba2);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }
                
                h1 {
                    font-size: 2.5rem;
                    margin-bottom: 10px;
                }
                
                .balance {
                    font-size: 1.8rem;
                    font-weight: bold;
                    background: rgba(255,255,255,0.2);
                    padding: 10px 30px;
                    border-radius: 50px;
                    display: inline-block;
                    margin-top: 15px;
                }
                
                .session-info {
                    font-size: 0.9rem;
                    opacity: 0.8;
                    margin-top: 10px;
                    font-family: monospace;
                }
                
                .content {
                    display: flex;
                    flex-wrap: wrap;
                    min-height: 500px;
                }
                
                .products-section {
                    flex: 3;
                    padding: 30px;
                    background: #f8f9fa;
                }
                
                .cart-section {
                    flex: 2;
                    padding: 30px;
                    background: white;
                    border-left: 3px dashed #e0e0e0;
                    display: flex;
                    flex-direction: column;
                }
                
                h2 {
                    color: #333;
                    margin-bottom: 25px;
                    padding-bottom: 15px;
                    border-bottom: 2px solid #667eea;
                }
                
                .cart-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 20px;
                }
                
                .clear-cart-btn {
                    background: #ffa502;
                    color: white;
                    border: none;
                    padding: 8px 15px;
                    border-radius: 6px;
                    cursor: pointer;
                    font-weight: 600;
                    transition: all 0.3s ease;
                    font-size: 0.9rem;
                }
                
                .clear-cart-btn:hover {
                    background: #ff7b00;
                    transform: scale(1.05);
                }
                
                .product-list {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                    gap: 20px;
                    margin-top: 20px;
                }
                
                .product-card {
                    background: white;
                    border-radius: 15px;
                    padding: 25px;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
                    transition: all 0.3s ease;
                    border: 2px solid transparent;
                    text-align: center;
                    cursor: pointer;
                }
                
                .product-card:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 15px 30px rgba(0,0,0,0.15);
                    border-color: #667eea;
                }
                
                .product-name {
                    font-size: 1.3rem;
                    color: #333;
                    margin-bottom: 10px;
                    font-weight: 600;
                }
                
                .product-price {
                    color: #764ba2;
                    font-size: 1.5rem;
                    font-weight: bold;
                    margin: 15px 0;
                }
                
                .buy-button {
                    background: linear-gradient(90deg, #667eea, #764ba2);
                    color: white;
                    border: none;
                    padding: 12px 25px;
                    border-radius: 8px;
                    font-size: 1rem;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    width: 100%;
                }
                
                .buy-button:hover:not(:disabled) {
                    transform: scale(1.05);
                    box-shadow: 0 5px 15px rgba(102,126,234,0.4);
                }
                
                .buy-button:disabled {
                    background: #cccccc;
                    cursor: not-allowed;
                    opacity: 0.7;
                }
                
                .cart-items {
                    min-height: 200px;
                    flex-grow: 1;
                    overflow-y: auto;
                    max-height: 300px;
                    padding-right: 10px;
                }
                
                .cart-items::-webkit-scrollbar {
                    width: 6px;
                }
                
                .cart-items::-webkit-scrollbar-track {
                    background: #f1f1f1;
                    border-radius: 3px;
                }
                
                .cart-items::-webkit-scrollbar-thumb {
                    background: #667eea;
                    border-radius: 3px;
                }
                
                .cart-item {
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 10px;
                    margin-bottom: 15px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    animation: fadeIn 0.3s ease;
                }
                
                @keyframes fadeIn {
                    from { opacity: 0; transform: translateX(-10px); }
                    to { opacity: 1; transform: translateX(0); }
                }
                
                .remove-button {
                    background: #ff4757;
                    color: white;
                    border: none;
                    padding: 8px 15px;
                    border-radius: 6px;
                    cursor: pointer;
                    font-weight: 600;
                    transition: all 0.3s ease;
                }
                
                .remove-button:hover {
                    background: #ff3742;
                    transform: scale(1.05);
                }
                
                .cart-summary {
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 2px solid #e0e0e0;
                }
                
                .summary-row {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 10px;
                    font-size: 1.1rem;
                }
                
                .summary-row .total-amount {
                    font-size: 1.5rem;
                    font-weight: bold;
                    color: #764ba2;
                }
                
                .cart-actions {
                    margin-top: 25px;
                }
                
                .checkout-button {
                    background: linear-gradient(90deg, #00b09b, #96c93d);
                    color: white;
                    border: none;
                    padding: 15px 30px;
                    border-radius: 10px;
                    font-size: 1.1rem;
                    font-weight: 600;
                    cursor: pointer;
                    width: 100%;
                    transition: all 0.3s ease;
                }
                
                .checkout-button:hover:not(:disabled) {
                    transform: scale(1.05);
                    box-shadow: 0 5px 20px rgba(0,176,155,0.4);
                }
                
                .checkout-button:disabled {
                    background: #cccccc;
                    cursor: not-allowed;
                }
                
                .shop-controls {
                    margin-top: auto;
                    padding-top: 30px;
                    border-top: 2px dashed #e0e0e0;
                }
                
                .shop-controls h3 {
                    color: #333;
                    margin-bottom: 15px;
                    font-size: 1.2rem;
                }
                
                .control-buttons {
                    display: flex;
                    gap: 15px;
                }
                
                .exit-btn {
                    background: linear-gradient(90deg, #ff7e5f, #feb47b);
                    color: white;
                    border: none;
                    padding: 12px 25px;
                    border-radius: 8px;
                    font-size: 1rem;
                    font-weight: 600;
                    cursor: pointer;
                    width: 100%;
                    transition: all 0.3s ease;
                }
                
                .exit-btn:hover {
                    transform: scale(1.05);
                    box-shadow: 0 5px 15px rgba(255,126,95,0.4);
                }
                
                .empty-cart {
                    text-align: center;
                    color: #888;
                    padding: 40px 20px;
                    font-style: italic;
                    font-size: 1.1rem;
                }
                
                @media (max-width: 768px) {
                    .content {
                        flex-direction: column;
                    }
                    
                    .cart-section {
                        border-left: none;
                        border-top: 3px dashed #e0e0e0;
                    }
                    
                    .product-list {
                        grid-template-columns: 1fr;
                    }
                    
                    .cart-header {
                        flex-direction: column;
                        align-items: flex-start;
                        gap: 10px;
                    }
                    
                    .clear-cart-btn {
                        align-self: flex-end;
                    }
                }
            `;
            document.head.appendChild(style);
        }
    }
    
    updateDisplay() {
        // Обновляем баланс
        const balanceElements = document.querySelectorAll('.balance-amount');
        balanceElements.forEach(element => {
            element.textContent = this.balance.toLocaleString();
        });
        
        // Обновляем количество товаров в корзине
        const cartCount = document.querySelector('.cart-count');
        if (cartCount) {
            cartCount.textContent = this.cart.length;
        }
        
        // Обновляем итоговую сумму
        const totalAmount = document.querySelector('.total-amount');
        if (totalAmount) {
            totalAmount.textContent = this.calculateTotal().toLocaleString();
        }
        
        // Обновляем кнопки покупки
        document.querySelectorAll('.buy-button').forEach((btn, index) => {
            const product = this.products[index];
            btn.disabled = this.balance < product.price;
            btn.textContent = this.balance >= product.price ? TEXTS.addToCart : TEXTS.insufficientFunds;
        });
        
        // Обновляем отображение корзины
        const cartItems = document.querySelector('.cart-items');
        const cartSummary = document.querySelector('.cart-summary');
        const cartHeader = document.querySelector('.cart-header');
        
        if (this.cart.length === 0) {
            if (cartItems) {
                cartItems.innerHTML = `<div class="empty-cart">${TEXTS.emptyCart}</div>`;
            }
            if (cartSummary) {
                cartSummary.remove();
            }
            if (cartHeader && cartHeader.querySelector('.clear-cart-btn')) {
                cartHeader.querySelector('.clear-cart-btn').remove();
            }
        } else {
            if (cartItems) {
                cartItems.innerHTML = this.cart.map(item => `
                    <div class="cart-item" data-id="${item.id}">
                        <div>
                            <div class="product-name">${item.showName}</div>
                            <div class="product-price">${item.price.toLocaleString()} ${TEXTS.currency}</div>
                        </div>
                        <button class="remove-button" data-id="${item.id}" data-price="${item.price}">
                            ${TEXTS.remove}
                        </button>
                    </div>
                `).join('');
            }
            
            // Добавляем кнопку очистки корзины в заголовок
            if (cartHeader && !cartHeader.querySelector('.clear-cart-btn')) {
                const clearBtn = document.createElement('button');
                clearBtn.className = 'clear-cart-btn';
                clearBtn.title = TEXTS.hintClearCart;
                clearBtn.textContent = TEXTS.clearCart;
                cartHeader.appendChild(clearBtn);
                
                clearBtn.addEventListener('click', () => this.clearCart());
            }
            
            // Добавляем или обновляем summary
            if (!cartSummary && document.querySelector('.cart-section')) {
                const cartSection = document.querySelector('.cart-section');
                const summaryHTML = `
                    <div class="cart-summary">
                        <div class="summary-row">
                            <span>${TEXTS.totalAmount}</span>
                            <span class="total-amount">${this.calculateTotal().toLocaleString()} ${TEXTS.currency}</span>
                        </div>
                        <div class="summary-row">
                            <span>${TEXTS.availableBalance}:</span>
                            <span class="balance-amount">${this.balance.toLocaleString()} ${TEXTS.currency}</span>
                        </div>
                        <div class="cart-actions">
                            <button class="checkout-button" title="${TEXTS.hintCheckout}">
                                ${TEXTS.checkout}
                            </button>
                        </div>
                    </div>
                `;
                const shopControls = document.querySelector('.shop-controls');
                if (shopControls) {
                    shopControls.insertAdjacentHTML('beforebegin', summaryHTML);
                } else {
                    cartSection.insertAdjacentHTML('beforeend', summaryHTML);
                }
            }
        }
        
        this.saveState();
    }
    
    bindEvents() {
        document.addEventListener('click', (e) => {
            // Добавление в корзину
            if (e.target.classList.contains('buy-button')) {
                const index = parseInt(e.target.dataset.index);
                if (!isNaN(index) && this.products[index]) {
                    this.addToCart(this.products[index]);
                }
            }
            
            // Удаление из корзины
            if (e.target.classList.contains('remove-button')) {
                const id = parseInt(e.target.dataset.id);
                const price = parseInt(e.target.dataset.price);
                if (!isNaN(id) && !isNaN(price)) {
                    this.removeFromCart(id, price);
                }
            }
            
            // Оформление заказа
            if (e.target.classList.contains('checkout-button')) {
                this.checkout();
            }
            
            // Очистка корзины
            if (e.target.classList.contains('clear-cart-btn')) {
                this.clearCart();
            }
            
            // Выход
            if (e.target.classList.contains('exit-btn')) {
                this.exitShop();
            }
        });
        
        // Обработка кликов на карточки товаров
        document.addEventListener('click', (e) => {
            const productCard = e.target.closest('.product-card');
            if (productCard && !e.target.classList.contains('buy-button')) {
                const index = productCard.querySelector('.buy-button')?.dataset.index;
                if (index !== undefined && this.products[index]) {
                    this.addToCart(this.products[index]);
                }
            }
        });
    }
}

// Запуск магазина
document.addEventListener('DOMContentLoaded', () => {
    window.shop = new Shop();
    
    // Обработка сообщений от родительского окна (если есть)
    window.addEventListener('message', (event) => {
        if (event.data === 'shop_exit') {
            window.close();
        }
    });
});