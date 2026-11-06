/**
 * dashboard.js - Reservado para la inicialización de gráficos y widgets.
 *
 * Los contenedores [data-widget] del dashboard quedan listos para
 * integrarse con una librería de gráficos en la siguiente fase.
 */
(function () {
    "use strict";

    function initWidgets() {
        const containers = document.querySelectorAll("[data-widget]");
        containers.forEach((container) => {
            container.dataset.widgetReady = "true";
        });
    }

    if (window.App) {
        window.App.register("dashboard", initWidgets);
    } else {
        document.addEventListener("DOMContentLoaded", initWidgets);
    }
})();
