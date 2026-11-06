/**
 * inventory.js - Mejoras de interfaz para el módulo de inventario.
 *
 * Se registra sobre el objeto global App definido en main.js.
 */
(function () {
    "use strict";

    const TABLE_SELECTOR = '[data-module="inventory"]';

    /** Confirma antes de eliminar un producto desde el listado. */
    function initDeleteConfirmation() {
        const table = document.querySelector(TABLE_SELECTOR);
        if (!table) {
            return;
        }
        table.addEventListener("click", (event) => {
            const link = event.target.closest(".btn--danger");
            if (!link) {
                return;
            }
            const confirmed = window.confirm(
                "¿Seguro que deseas eliminar este producto?"
            );
            if (!confirmed) {
                event.preventDefault();
            }
        });
    }

    if (window.App) {
        window.App.register("inventory", initDeleteConfirmation);
    }
})();
