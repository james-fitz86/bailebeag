console.log("base JS loaded");

document.addEventListener('DOMContentLoaded', () => {
    const navButton = document.querySelector(".navbar-toggler");
    const navBar = document.querySelector(".navbar-collapse");

    navButton.addEventListener("click", function(){
        navBar.classList.toggle("show");
    });
});