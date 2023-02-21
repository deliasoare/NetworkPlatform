document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('#post').forEach(post => {
        post.style.display = 'block';
    })
    document.querySelectorAll('#form').forEach(form => {
        form.style.display = 'none';
        
    })
    document.querySelectorAll('.post').forEach(post => {
        const id = post.querySelector('#post').className;
        if (post.querySelector('#edit')) {
            post.querySelector('#edit').onclick = function() {
                post.querySelector('#post').style.display = 'none';
                post.querySelector('#form').style.display = 'block';
    
                post.querySelector('#save').onclick = function() {
                    const content = post.querySelector('textarea').value;
                    fetch(`/post/${id}`, {
                        method: "PUT",
                        body: JSON.stringify({
                            content:content
                        })
                    })
                    post.querySelector('#form').style.display = 'none';
                    post.querySelector('#body').innerHTML = content;
                    post.querySelector('#post').style.display = 'block';
                }
            }
        }
        post.querySelector('#like').onclick = function() {
            fetch(`/likes`, {
                method:"POST",
                body:JSON.stringify({
                    liker: post.querySelector('#like').className,
                    post_id : parseInt(id)
                })
            })
            .then(response =>response.json())
            .then(result => {
                likes = post.querySelector('#likes')
                like = post.querySelector('#like')
                if (result.successfull == 'added') {
                    likes.innerHTML = parseInt(likes.innerHTML) + 1;
                    like.innerHTML = '&#x2665;'
                }
                else {
                    likes.innerHTML = parseInt(likes.innerHTML) - 1;
                    like.innerHTML = '♡';
                }
            });

        }
    })
})