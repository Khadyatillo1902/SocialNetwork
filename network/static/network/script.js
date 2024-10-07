document.addEventListener('DOMContentLoaded', function() {
    const editPosts = document.querySelectorAll('.edit-post'); // Get all edit-post buttons
    const returnButtons = document.querySelectorAll('.return-post');

    
        
    document.querySelectorAll('.like-btn').forEach(button => {
        button.onclick = () => {
            const postId = button.dataset.id;
            fetch(`/posts/${postId}/like`, {
                method: "PUT",
                headers: {
                    "X-CSRFToken": getCookie('csrftoken'),
                },
            })
            .then(response => response.json())
            .then(result => {
                document.querySelector(`#like-count-${postId}`).innerHTML = result.like_count;
                button.innerHTML = result.liked ? 'Unlike': 'Like';
            });
        };
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    editPosts.forEach((editPost) => {
        editPost.addEventListener('click', function() {
            const postId = editPost.dataset.id;
            const postContent = document.querySelector(`.post-content-${postId}`);
            
            // Show edit controls and hide the edit button
            const editControls = editPost.previousElementSibling; // Use previousElementSibling to target the correct edit-controls div
            editPost.style.display = 'none'; // Hide the edit button
            editControls.style.display = 'block'; // Show the edit controls (textarea and buttons)

            // Fill the textarea with current post content
            const textarea = editControls.querySelector('.edit-content');
            textarea.value = postContent.textContent.trim(); // Make sure the content is correctly trimmed

            const saveButton = editControls.querySelector('.save-edit');

            // Event listener for saving the edited post
            saveButton.addEventListener('click', function() {
                const newContent = textarea.value.trim();
                if (newContent === '') {
                    alert("Content cannot be empty");
                    return;
                }

                fetch(`/posts/${postId}/edit`, {
                    method: 'PUT',
                    body: JSON.stringify({ content: newContent }),
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                    }
                })
                .then(response => response.json())
                .then(result => {
                    if (result.error) {
                        alert(result.error);
                    } else {
                        postContent.innerHTML = result.new_content;
                        editControls.style.display = 'none'; // Hide the edit controls
                        editPost.style.display = 'block'; // Show the edit button again
                    }
                })
                .catch(error => console.log('Error:', error));
            });
        });
    });

    returnButtons.forEach((returnButton) => {
        returnButton.addEventListener('click', function() {
            const editControls = returnButton.parentElement;
            const editPostButton = editControls.nextElementSibling; // Find the corresponding edit button

            editControls.style.display = 'none'; // Hide edit controls
            editPostButton.style.display = 'block'; // Show the edit button again
        });
    });

    document.querySelectorAll('.comment-button').forEach(commentButton => {
        commentButton.addEventListener('click', function() {
            console.log('hello');
            const postId = commentButton.dataset.id;
            const newComment = document.querySelector(`.comment-content`).value.trim();
    
            if (!newComment) {
                alert("Comment content cannot be empty");
                return;
            }
    
            fetch(`posts/${postId}/comment`, {
                method: "POST",
                body: JSON.stringify({'content': newComment}),
                headers: {
                    "X-CSRFToken": getCookie('csrftoken'),
                    "Content-Type": "application/json"
                },
            })
            .then(response => response.json())
            .then(result => {
                document.querySelector(`.comment-content`).value = ''; // clear textarea after submission
                document.querySelector('.comment-user').innerHTML = result.user;
                document.querySelector('.comment-content').innerHTML = result.content;
                document.querySelector('.comment-date').innerHTML = result.date;
                if (result.error) {
                    console.log(result.error);
                } else {
                    // Optional: Handle the result, e.g., add the new comment to the UI
                    console.log(result);
                }
            });
        });
    });
});