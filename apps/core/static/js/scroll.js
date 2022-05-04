let spin = document.querySelector('.spinner');
spin.style.opacity = '0';

let ias = new InfiniteAjaxScroll("#data", {
  item: ".item",
  next: ".next",
  pagination: ".pagination",
  spinner: '.spinner',
});

ias.on('next', function() {
  let spinner = document.querySelector('.spinner');
  spinner.style.opacity = '1'; 
});

ias.on('last', function() {
  let el = document.querySelector('.no-more');
  el.style.opacity = '1';
});