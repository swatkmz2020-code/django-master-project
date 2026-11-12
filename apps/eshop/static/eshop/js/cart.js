import { productAction } from './utils.js'

class CartManager {
    constructor() {
        this.cartCounter = document.getElementById('cartCounter')
        this.init()
    }

    init() {
        document.addEventListener('click', (e) => {
            // 1. Добавление в корзину со страницы товаров
            const addBtn = e.target.closest('.add-to-cart-btn')
            if (addBtn) {
                e.preventDefault()
                this.handleAddToCart(addBtn)
                return
            }

            // 2. Изменение количества (+ / -) и удаление внутри корзины
            const cartActionBtn = e.target.closest('.js-cart-action')
            if (cartActionBtn) {
                e.preventDefault()
                this.handleCartAction(cartActionBtn)
            }
        })
    }

    async handleAddToCart(button) {
        const url = button.dataset.url
        if (!url) return

        button.disabled = true

        try {
            const data = await productAction(url)

            if (data && data.success) {
                if (this.cartCounter) {
                    this.cartCounter.textContent = data.cart_count
                }

                const originalHTML = button.innerHTML
                button.classList.replace('btn-primary', 'btn-success')
                button.textContent = 'В корзине ✓'

                setTimeout(() => {
                    button.classList.replace('btn-success', 'btn-primary')
                    button.innerHTML = originalHTML
                    button.disabled = false
                }, 1000)
            } else {
                button.disabled = false
            }
        } catch (error) {
            console.error('Ошибка при добавлении в корзину:', error)
            button.disabled = false
        }
    }

    async handleCartAction(button) {
        const url = button.dataset.url
        if (!url) return

        const row = button.closest('tr')
        button.disabled = true

        try {
            const data = await productAction(url)

            if (data && data.success) {
                // Обновляем строку товара или удаляем её
                if (data.item_quantity === 0) {
                    row.remove()
                } else {
                    row.querySelector('.js-item-quantity').textContent = `${data.item_quantity} шт.`
                    row.querySelector('.js-item-total').textContent = data.item_total_price
                }

                // Обновляем "Итого" на странице корзины
                const totalPriceEl = document.getElementById('cart-total-price')
                if (totalPriceEl) {
                    totalPriceEl.textContent = data.cart_total_price
                }

                // Обновляем счётчик в шапке
                if (this.cartCounter) {
                    this.cartCounter.textContent = data.cart_count
                }

                // Если корзина опустела — показываем сообщение
                if (data.cart_count === 0) {
                    const cartContent = document.getElementById('cart-content')
                    const emptyMsg = document.getElementById('empty-cart-message')
                    if (cartContent) cartContent.remove()
                    if (emptyMsg) emptyMsg.classList.remove('d-none')
                }
            }
        } catch (error) {
            console.error('Ошибка при обновлении корзины:', error)
        } finally {
            button.disabled = false
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new CartManager()
})

