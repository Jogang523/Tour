document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('updatePostForm');
    const titleInput = document.getElementById('postTitle');
    const contentInput = document.getElementById('postContent');
    const imageInput = document.getElementById('postImage');
    const imagePreview = document.getElementById('imagePreview');
    const previewImage = document.getElementById('previewImage');
    const deleteImageBtn = document.getElementById('deleteImage');
    const backButton = document.getElementById('backButton');

    // URL에서 직접 postId 추출
    const postId = window.location.pathname.split('/').pop();

    async function fetchPost() {
        try {
            const response = await fetch(`/api/post/${postId}`, {
                method: 'GET',
                credentials: 'include'
            });
            if (!response.ok) {
                throw new Error('서버 응답이 올바르지 않습니다.');
            }
            const post = await response.json();
            
            titleInput.value = post.title;
            contentInput.value = post.content;
            if (post.image_url) {
                previewImage.src = post.image_url;
                imagePreview.style.display = 'block';
            }
        } catch (error) {
            console.error('Error fetching post:', error);
            alert('게시글을 불러오는 중 오류가 발생했습니다.');
        }
    }

    fetchPost();

    imageInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImage.src = e.target.result;
                imagePreview.style.display = 'block';
            }
            reader.readAsDataURL(file);
        }
    });

    deleteImageBtn.addEventListener('click', function() {
        imageInput.value = '';
        previewImage.src = '';
        imagePreview.style.display = 'none';
    });

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const formData = new FormData();
        formData.append('title', titleInput.value);
        formData.append('content', contentInput.value);
        if (imageInput.files[0]) {
            formData.append('image', imageInput.files[0]);
        }
        if (imagePreview.style.display === 'none') {
            formData.append('delete_image', 'true');
        }

        try {
            const response = await fetch(`/boardupdate/${postId}`, {
                method: 'POST',
                body: formData,
                credentials: 'include'
            });

            if (response.ok) {
                const result = await response.json();
                alert(result.message);
                window.location.href = `/post/${postId}`;
            } else {
                const errorData = await response.text();
                alert('게시글 수정 실패: ' + errorData);
            }
        } catch (error) {
            console.error('Error updating post:', error);
            alert('게시글 수정 중 오류가 발생했습니다.');
        }
    });

    backButton.addEventListener('click', function(e) {
        e.preventDefault();
        window.history.back();
    });
});