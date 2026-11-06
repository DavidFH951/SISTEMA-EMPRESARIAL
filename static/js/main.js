/**
 * main.js - Punto de entrada del JavaScript de la aplicación.
 *
 * Inicializa el comportamiento global (menú lateral, mensajes flash) y
 * expone un pequeño registro de módulos para futuras extensiones.
 */
(function () {
    "use strict";

    /** Registro central de módulos de la aplicación. */
    const App = {
        modules: {},

        register(name, initializer) {
            this.modules[name] = initializer;
        },

        init() {
            Object.values(this.modules).forEach((initializer) => {
                try {
                    initializer();
                } catch (error) {
                    console.error("Error al inicializar módulo:", error);
                }
            });
        },
    };

    /** Alterna la visibilidad del menú lateral en pantallas pequeñas. */
    function initSidebarToggle() {
        const toggle = document.querySelector("[data-sidebar-toggle]");
        const sidebar = document.querySelector("[data-sidebar]");
        if (!toggle || !sidebar) {
            return;
        }
        toggle.addEventListener("click", () => {
            sidebar.classList.toggle("is-collapsed");
        });
    }

    /** Oculta automáticamente los mensajes flash tras unos segundos. */
    function initFlashMessages() {
        const messages = document.querySelectorAll(".messages .alert");
        messages.forEach((message) => {
            window.setTimeout(() => {
                message.classList.add("is-hidden");
            }, 5000);
        });
    }

    App.register("sidebar", initSidebarToggle);
    App.register("messages", initFlashMessages);

    document.addEventListener("DOMContentLoaded", () => App.init());

    window.App = App;
})();
