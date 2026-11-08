import { productAction } from "../../../../static/eshop/js/utils.js";
import { formatDate } from "../../../../static/js/format-dates.js";

const commentFormElement = document.getElementById('commentForm');
commentFormElement.addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const url = this.dataset.addCommentUrl;

    // Скрываем предыдущие ошибки
    const commentErrorsElement = document.getElementById('commentErrors');
    commentErrorsElement.classList.add('d-none');
    commentErrorsElement.textContent = '';

    try {
        const data = await productAction(url, formData);

        if (data.success) {
            // Очищаем текстовое поле
            this.querySelector('textarea').value = '';

            // Добавляем новый отзыв в начало списка
            const commentsListElement = document.getElementById('commentsList');
            const emptyMessageElement = commentsListElement.querySelector('#emptyMessage');

            if (emptyMessageElement) {
                emptyMessageElement.remove();
            }
            commentsListElement.insertAdjacentHTML('afterbegin', data.comment_html);

            const newCommentElement = commentsListElement.firstElementChild;
            const dateElement = newCommentElement.querySelector('.date-field');
            formatDate(dateElement);

            // УВЕЛИЧИВАЕМ offset на 1, так как добавили новый отзыв
            window.commentsBatchLoader.offset += 1

            // Обновляем счетчик отзывов в заголовке
            const commentsTitleElement = document.querySelector('#commentsTitle');
            commentsTitleElement.textContent = `Отзывы (${data.comments_count})`;
        } else {
            // Показываем ошибку
            commentErrorsElement.textContent = data.error;
            commentErrorsElement.classList.remove('d-none');
        }
    } catch (error) {
        console.error('Ошибка при добавлении отзыва:', error);
        commentErrorsElement.textContent = 'Произошла ошибка при отправке отзыва';
        commentErrorsElement.classList.remove('d-none');
    }
});
