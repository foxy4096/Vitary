$("#body").keydown(function () {
  var text = $("#body").val();
  // console.log(text);
  var word = text.split(" ").reverse()[0];
  // console.log(word)
  if (word.charAt(0) == "@" && word.length > 3) {
    $.ajax({
      url: "/api/v1/users/search/",
      method: "GET",
      data: {
        query: word.replace("@", ""),
      },
      headers: {
        "X-CSRFToken": "{{ csrf_token }}",
      },
      success: function (data) {
        $("#users_drop").toggleClass("is-hidden");
        let html_content = `
                            ${data.users.map(
                              (user) =>
                                `
                                <div class="media item">
                                    <div class="media-left">
                                        <article class='image is-32x32'>
                                            <img src='${user.image}' class='is-rounded'>
                                        </article>
                                    </div>
                                    <div class="media-content">
                                        <h4 class="title is-4">
                                        <strong>
                                        ${user.first_name} ${user.last_name}
                                        </strong>
                                        </h4>
                                        <p class="subtitle is-6 mb-0"><a role='button' onclick='ins("${user.username}")'>@${user.username}</a></p>
                                    </div>
                                    <div class='media-right'>
                                        <a role='button' onclick='ins("${user.username}")' class='button is-primary'>Add</a>
                                    </div>
                                </div>
                                `
                            )}
                            `;
        $("#users_drop").html(html_content.toString().replace(",", ""));
      },
    });
  }
});

function ins(username) {
  var text = $("#body").val();
  var word = text.split(" ").reverse()[0];
  // console.log(word)
  processChange();
  $("#body").val(
    $("#body")
      .val()
      .replace(word, "@" + username)
  );
  $("#body").focus();
}
