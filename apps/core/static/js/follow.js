function follow(username) {
  $.ajax({
    url: `/api/v1/follow/?username=${username}`,
    type: "GET",
    success: function (data) {
      console.log(data);
      if (data.follow === true) {
        $("#follow_" + username).text("Unfollow ➖");
        $("#follower_count").text(parseInt($("#follower_count").text()) + 1);
      } else if (data.follow === false) {
        $("#follow_" + username).text("Follow ➕");
        $("#follower_count").text(parseInt($("#follower_count").text()) - 1);
      }
      try {
        document.querySelector("#followModal").classList.toggle("is-active");
      } catch (err) {
        return
      }
    },
  });
}
