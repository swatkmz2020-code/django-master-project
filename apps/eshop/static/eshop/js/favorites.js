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

        // 1. Сначала железно отправляем запрос на бэкенд и ждем ответа базы данных
        const data = await productAction(url)
        
        // 2. Только после получения ответа меняем визуальное состояние
        if (data.is_favorite) {
            iconEmpty?.classList.add('d-none')
            iconFilled?.classList.remove('d-none')
        } else {
            iconEmpty?.classList.remove('d-none')
            iconFilled?.classList.add('d-none')
            
            // Если товар больше не в избранном и мы на странице Избранного — удаляем карточку
            if (productCardElement) {
                removeProductFromFavorites(productCardElement)
            }
        }
        
        // 3. Обновляем счетчик лайков числом, которое пришло из базы данных
        if (favoritesCountElement) {
            favoritesCountElement.textContent = data.favorites_count
        }
    }
})

// Функция для плавного удаления товара со страницы избранных
function removeProductFromFavorites(productCardElement) {
    const favoriteContainer = document.querySelector('[data-page-type="favorite-products"]')
    
    if (favoriteContainer !== null) { 
        // Находим родительскую обертку всей карточки в сетке, чтобы не ломать структуру сетки Grid
        const cardWrapper = productCardElement.closest('.product-container-wrapper') || productCardElement;
        
        // Удаляем элемент с экрана
        cardWrapper.remove()

        // Проверяем, остались ли товары в сетке
        const remainingProducts = favoriteContainer.querySelectorAll('.product-container')
        if (remainingProducts.length === 0) {
            const gridContainer = favoriteContainer.querySelector('.products-grid')
            if (gridContainer) {
                gridContainer.innerHTML = '<p class="text-center w-100">Пока нет избранных товаров.</p>'
            }
        }
    }
}
