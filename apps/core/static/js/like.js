function like_vit(vit_id) {
    fetch(`/api/v1/vit/like/?vit_pk=${vit_id}`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
            'type': 'application/json'
        },
    }).then(function (response) {
        return response.json();
    }).then(function (data) {
        if (data.status == 'success') {
            var like_count = document.getElementById('like_count_' + vit_id);
            like_count.innerHTML = data.like_count;
            var like_count = document.getElementById('like_count_' + vit_id);
            like_count.innerHTML = data.likes;
            if (data.liked) {
                var like_icon = document.getElementById('vit_like_' + vit_id + '_icon');
                like_icon.setAttribute('fill', '#ff0000');
            } else {
                var like_icon = document.getElementById('vit_like_' + vit_id + '_icon');
                like_icon.setAttribute('fill', '#000000');
            }
        }
    });
}