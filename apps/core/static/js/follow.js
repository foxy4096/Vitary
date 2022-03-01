function follow(username){
    $.ajax({
        url: '/api/v1/follow/',
        type: 'GET',
        
        data:{
            'username': username
        },
        success: function (data){
            console.log(data)
            if (data.follow === true){
                $('#follow_' + username).text("Unfollow ➖");
            }
            else if (data.follow === false){
                $('#follow_' + username).text("Follow ➕");

            }
            
        }
    })
}