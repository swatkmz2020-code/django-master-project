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

            // Добавляем новый комментарий в начало списка
            const commentsListElement = document.getElementById('commentsList');
            const emptyMessageElement = commentsListElement.querySelector('#emptyMessage');

            if (emptyMessageElement) {
                emptyMessageElement.remove();
            }
            commentsListElement.insertAdjacentHTML('afterbegin', data.comment_html);

            const newCommentElement = commentsListElement.firstElementChild;
            const dateElement = newCommentElement.querySelector('.date-field');
            formatDate(dateElement);

            // Обновляем счетчик комментариев в заголовке
            const commentsTitleElement = document.querySelector('#commentsTitle');
            commentsTitleElement.textContent = `Комментарии (${data.comments_count})`;
        } else {
            // Показываем ошибку
            commentErrorsElement.textContent = data.error;
            commentErrorsElement.classList.remove('d-none');
        }
    } catch (error) {
        console.error('Ошибка при добавлении комментария:', error);
        commentErrorsElement.textContent = 'Произошла ошибка при отправке комментария';
        commentErrorsElement.classList.remove('d-none');
    }
});
