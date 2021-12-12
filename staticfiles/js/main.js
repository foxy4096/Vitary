function like_feed(feed_id) {
    fetch("{% url 'like_feed' %}", {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({
            feed_id: feed_id
        })
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