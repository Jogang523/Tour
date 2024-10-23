document.addEventListener('DOMContentLoaded', function() {
    const deleteButton = document.getElementById('deletePost');
    const modal = document.getElementById('passwordModal');
    const passwordInput = document.getElementById('passwordInput');
    const confirmButton = document.getElementById('confirmDelete');
    const cancelButton = document.getElementById('cancelDelete');
    const closeButton = document.getElementsByClassName('close')[0];

    if (deleteButton) {
        deleteButton.addEventListener('click', function(e) {
            e.preventDefault();
            modal.style.display = "block";
        });
    }

    cancelButton.addEventListener('click', function() {
        modal.style.display = "none";
        passwordInput.value = '';
    });

    closeButton.addEventListener('click', function() {
        modal.style.display = "none";
        passwordInput.value = '';
    });

    confirmButton.addEventListener('click', function() {
        const password = passwordInput.value;
        if (password) {
            fetch('/verify-password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    post_id: '{{ post.id }}',
                    password: password
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    return fetch('/delete-post/{{ post.id }}', {
                        method: 'POST',
                    });
                } else {
                    alert('비밀번호가 일치하지 않습니다.');
                    throw new Error('Password incorrect');
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('게시글이 삭제되었습니다.');
                    window.location.href = '/board';
                } else {
                    alert('게시글 삭제에 실패했습니다.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            })
            .finally(() => {
                modal.style.display = "none";
                passwordInput.value = '';
            });
        }
    });

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
            passwordInput.value = '';
        }
    }
});
