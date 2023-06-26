document.addEventListener("DOMContentLoaded", () => {
  (document.querySelectorAll(".notification .delete") || []).forEach(
    ($delete) => {
      const $notification = $delete.parentNode;

      $delete.addEventListener("click", () => {
        $notification.parentNode.removeChild($notification);
      });
    }
  );
});

$(".message-header>.delete").click(function () {
  $(this).parent().parent().remove();
});

function debounce(func, timeout = 300) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => {
      func.apply(this, args);
    }, timeout);
  };
}

document.addEventListener("keydown", function (e) {
  if (e.ctrlKey && e.keyCode == 81) {
    toggleSearch();
  }
});

document.addEventListener("keydown", function (e) {
  if (e.keyCode == 27) {
    toggleSearch();
  }
});
function toggleSearch() {
  document.getElementById("searchModal").classList.toggle("is-active");
  document.querySelector("#search").focus();
}

