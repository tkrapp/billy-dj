window.billyShared = {
    showModal(selector) {
        let modalElement = document.querySelector(selector);
        let modal = bootstrap.Modal.getOrCreateInstance(modalElement);

        modal.show();
    },
    hideModal(selector) {
        console.log(selector);
        let modalElement = document.querySelector(selector);
        let modal = bootstrap.Modal.getOrCreateInstance(modalElement);

        modal.hide();
    },
    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(
                        cookie.substring(name.length + 1)
                    );
                    break;
                }
            }
        }
        return cookieValue;
    },
    closest(element, selector) {
        let result = null;
        while (
            !result &&
            (element = element.parentElement) instanceof HTMLElement
        ) {
            if (element.matches(selector)) result = element;
        }
        return result;
    },
    calcBruttoPrice(nettoPrice, vatRate) {
        return nettoPrice * (1 + vatRate / 100);
    },
    calcNettoPrice(bruttoPrice, vatRate) {
        return bruttoPrice / (1 + vatRate / 100);
    }
};

const csrftoken = billyShared.getCookie("csrftoken");

document.body.addEventListener("htmx:configRequest", (evt) => {
    evt.detail.headers["X-CSRFToken"] = csrftoken;
});
