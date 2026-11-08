import { getAction } from "./utils.js"
import { formatDatesInHTML } from "../../../../static/js/format-dates.js"

class BatchLoader {
    constructor(containerId) {
        this.container = document.getElementById(containerId)
        this.offset = Number(this.container.dataset.initialOffset)
        // Приводим строку к нижнему регистру, чтобы 'true' гарантированно совпало
        this.hasMore = this.container.dataset.hasMore.toLowerCase() === 'true'
        this.batchSize = Number(this.container.dataset.batchSize)
        this.loadMoreUrl = this.container.dataset.loadMoreUrl
        this.loading = false;

        this.init()
    }

    init() {
        window.addEventListener('scroll', () => {
            if ((window.scrollY + window.innerHeight) > (document.documentElement.scrollHeight - 1)) {
                this.loadMore()
            }
        });
    }

    async loadMore() {
        if (this.loading || !this.hasMore) return

        this.loading = true;
        document.getElementById("loadingSpinner")?.classList.remove("d-none")

        try {
            const data = await getAction(`${this.loadMoreUrl}?offset=${this.offset}`)
             // Форматируем даты
            const html = formatDatesInHTML(data.html)

            this.container.insertAdjacentHTML("beforeend", html)
            this.offset += this.batchSize
            this.hasMore = data.has_more
        } catch (error) {
            console.error("Ошибка загрузки:", error)
        } finally {
            this.loading = false;
            document.getElementById("loadingSpinner")?.classList.add("d-none")
        }
    }
}

export default BatchLoader
