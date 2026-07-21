"use strict";

const menuButton = document.querySelector("#menu-button");
const navigation = document.querySelector("#navigation");
const navigationLinks = document.querySelectorAll("#navigation a");
const yearElement = document.querySelector("#current-year");

function closeMenu() {
    if (!menuButton || !navigation) {
        return;
    }

    menuButton.classList.remove("is-open");
    navigation.classList.remove("is-open");
    menuButton.setAttribute("aria-expanded", "false");
    document.body.classList.remove("menu-open");
}

if (menuButton && navigation) {
    menuButton.addEventListener("click", () => {
        const menuIsOpen = navigation.classList.toggle("is-open");

        menuButton.classList.toggle("is-open", menuIsOpen);
        menuButton.setAttribute("aria-expanded", String(menuIsOpen));
        document.body.classList.toggle("menu-open", menuIsOpen);
    });
}

navigationLinks.forEach((link) => {
    link.addEventListener("click", closeMenu);
});

if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
}