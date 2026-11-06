/**
 * helpdesk.js - Interactividad de la Mesa de Ayuda.
 *
 * No se usa JavaScript en las plantillas: todo el comportamiento se
 * engancha desde este módulo a través de atributos `data-*`.
 */
(function () {
    "use strict";

    const MODULE_SELECTOR = '[data-module="helpdesk"]';
    // Estados que exigen confirmación antes de guardar la gestión.
    const CLOSING_STATUSES = ["RESOLVED", "CLOSED"];

    /** Localiza el formulario principal del bloque helpdesk de la página. */
    function findMainForm(scope) {
        if (scope.matches("form.form")) {
            return scope;
        }
        return scope.querySelector("form.form");
    }

    /** Confirma antes de marcar un ticket como resuelto o cerrado. */
    function initManageSafeguard(scope) {
        const form = findMainForm(scope);
        const statusSelect = form && form.querySelector('select[name="status"]');
        if (!statusSelect) {
            return;
        }

        form.addEventListener("submit", (event) => {
            if (!CLOSING_STATUSES.includes(statusSelect.value)) {
                return;
            }
            const label = statusSelect.options[statusSelect.selectedIndex].text;
            const confirmed = window.confirm(
                `¿Confirmas cambiar el ticket a "${label}"?`
            );
            if (!confirmed) {
                event.preventDefault();
            }
        });
    }

    /** Envía el formulario de filtros al cambiar un selector. */
    function initFilterAutoSubmit(scope) {
        const toolbar = scope.querySelector(".toolbar__search");
        if (!toolbar) {
            return;
        }
        toolbar.querySelectorAll("select").forEach((select) => {
            select.addEventListener("change", () => toolbar.submit());
        });
    }

    /** Marca los contenedores de widgets como listos para gráficos. */
    function initWidgetPlaceholders() {
        document.querySelectorAll("[data-widget]").forEach((container) => {
            container.dataset.widgetReady = "true";
        });
    }

    function init() {
        const scopes = document.querySelectorAll(MODULE_SELECTOR);
        scopes.forEach((scope) => {
            initManageSafeguard(scope);
            initFilterAutoSubmit(scope);
        });
        initWidgetPlaceholders();
    }

    if (window.App) {
        window.App.register("helpdesk", init);
    } else {
        document.addEventListener("DOMContentLoaded", init);
    }
})();
