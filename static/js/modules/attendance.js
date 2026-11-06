/**
 * attendance.js - Mejoras de interfaz para el módulo de asistencia.
 */
(function () {
    "use strict";

    const PANEL_SELECTOR = '[data-module="attendance"]';

    /** Muestra un reloj en vivo dentro del panel de asistencia. */
    function initLiveClock() {
        const panel = document.querySelector(PANEL_SELECTOR);
        if (!panel) {
            return;
        }
        const clock = panel.querySelector("[data-live-clock]");
        if (!clock) {
            return;
        }

        const update = () => {
            clock.textContent = new Date().toLocaleTimeString("es-PE");
        };
        update();
        window.setInterval(update, 1000);
    }

    if (window.App) {
        window.App.register("attendance", initLiveClock);
    }
})();
