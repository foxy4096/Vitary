function like_feed(feed_id) {
    fetch(`/api/v1/feed/like/?feed_pk=${feed_id}`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
            'type': 'application/json'
        },
    }).then(function (response) {
        return response.json();
    }).then(function (data) {
        if (data.status == 'success') {
            var like_count = document.getElementById('like_count_' + feed_id);
            like_count.innerHTML = data.like_count;
            var like_count = document.getElementById('like_count_' + feed_id);
            like_count.innerHTML = data.likes;
        }
    });
}