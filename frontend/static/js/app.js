"use strict";
document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("hello-btn");
    button?.addEventListener("click", () => {
        alert("Hello from TypeScript!");
    });
});
