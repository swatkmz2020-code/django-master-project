function getCookie(cookieKey) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(cookieKey + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(cookieKey.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export async function getAction(url) {
    const response = await fetch(url);

    if (!response.ok) {
        console.error("Request failed", response.status);
        return null;
    }

    return await response.json();
}

export async function productAction(url, bodyData = null) {
    // ОБЯЗАТЕЛЬНО добавляем "const response =" перед fetch
    const response = await fetch(url, {
        method: "POST",
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: bodyData // Не забудьте передать само тело (formData), иначе комментарий уйдет пустым
    });

    if (!response.ok) {
        console.error("Request failed", response.status);
        return null;
    }

    return await response.json();
}

