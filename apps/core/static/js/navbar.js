// document.addEventListener('DOMContentLoaded', () => {
            
//     // Get all "navbar-burger" elements
//     const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

//     // Check if there are any navbar burgers
//     if ($navbarBurgers.length > 0) {
        
//         // Add a click event on each of them
//         $navbarBurgers.forEach(el => {
//             el.addEventListener('click', () => {
                
//                 // Get the target from the "data-target" attribute
//                 const target = el.dataset.target;
//                 const $target = document.getElementById(target);
                
//                 // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
//                 el.classList.toggle('is-active');
//                 $target.classList.toggle('is-active');
                
//             });
//         });
//     }
    
// });

// Open the searchModal
function openSearch() {
    document.getElementById('searchModal').classList.add('is-active');
    document.getElementById('search').focus();
}

// Close the searchModal
function closeSearch() {
    document.getElementById('searchModal').classList.remove('is-active');
}

// run the openSearch if ctrl + q is pressed
document.addEventListener('keydown', function (e) {
    if (e.ctrlKey && e.keyCode == 81) {
        openSearch();
    }
});

// run the closeSearch if ESC is pressed
document.addEventListener('keydown', function (e) {
    if (e.keyCode == 27) {
        closeSearch();
    }
});