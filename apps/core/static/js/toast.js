let toasts = [];
const toastContainer = $("#toastContainer");

function createToast(message, extraStyles = "") {
  const toast = $(`
        <div class="toast" style="${extraStyles}">        
            <div class="toast-message">
                ${message}
            </div>
        </div>`);

  toastContainer.append(toast);

  toasts.push(toast);

  //   Remove the toast after 5 seconds
  setTimeout(() => {
    toast.remove();
    toasts.splice(toasts.indexOf(toast), 1);
  }, 5000);
}
