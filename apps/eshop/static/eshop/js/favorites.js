import { productAction } from "../../../../static/eshop/js/utils.js"

// Делегирование событий на контейнере
document.addEventListener('click', async (event) => {
    const favoriteBtnElement = event.target.closest('.favorite-btn')
    
    if (favoriteBtnElement) {
        const isAuthenticated = favoriteBtnElement.dataset.isAuthenticated === 'true'
        if (!isAuthenticated) {
            window.location.href = favoriteBtnElement.dataset.loginUrl
            return
        }

        const url = favoriteBtnElement.dataset.productFavoriteToggleUrl
        const productCardElement = favoriteBtnElement.closest('.product-container')

        // Находим обе иконки конкретно внутри этой кнопки
        const iconEmpty = favoriteBtnElement.querySelector('.icon-empty')
        const iconFilled = favoriteBtnElement.querySelector('.icon-filled')
        
        // Безопасный поиск счетчика: сначала в карточке, иначе внутри самой кнопки
        const favoritesCountElement = productCardElement 
            ? productCardElement.querySelector('.favorites-count') 
            : favoriteBtnElement.querySelector('.favorites-count')

        const data = await productAction(url)
        
        if (data.is_favorite) {
            iconEmpty?.classList.add('d-none')
            iconFilled?.classList.remove('d-none')
        } else {
            iconEmpty?.classList.remove('d-none')
            iconFilled?.classList.add('d-none')
            if (productCardElement) {
                removeProductFromFavorites(productCardElement)
            }
        }
        
        if (favoritesCountElement) {
            favoritesCountElement.textContent = data.favorites_count
        }
    }
})

// Функция для удаления товара со страницы избранных
function removeProductFromFavorites(productCardElement) {
    // Проверка, находимся ли на странице избранных (проверяем по data-атрибуту)
    if (document.querySelector('[data-page-type="favorite-products"]') !== null) { 
        // Удаляем карточку товара
        productCardElement.remove()

        // Проверяем, остались ли товары на странице
        const remainingProducts = document.querySelectorAll('.product-card')
        if (remainingProducts.length === 0) {
            // Показываем сообщение о пустом списке избранных
            const container = document.querySelector('.container')
            if (container) {
                container.innerHTML = '<p class="text-center">Пока нет избранных постов.</p>'
            }
        }
    }
}
