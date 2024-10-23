document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('createPostForm');
    const titleInput = document.getElementById('postTitle');
    const contentInput = document.getElementById('postContent');
    const imageInput = document.getElementById('postImage');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // 입력값 확인
        if (!titleInput.value.trim() || !contentInput.value.trim()) {
            alert('제목과 본문을 모두 입력해주세요.');
            return;
        }

        const formData = new FormData();
        formData.append('title', titleInput.value.trim());
        formData.append('content', contentInput.value.trim());
        if (imageInput.files[0]) {
            formData.append('image', imageInput.files[0]);
        }

        try {
            const response = await fetch('/write', {
                method: 'POST',
                body: formData,
                credentials: 'include'
            });

            if (response.ok) {
                alert('게시글이 성공적으로 작성되었습니다.');
                window.location.href = '/board';
            } else {
                const errorData = await response.json();
                alert('게시글 작성 실패: ' + (errorData.detail || '알 수 없는 오류'));
            }
        } catch (error) {
            console.error('Error creating post:', error);
            alert('게시글 작성 중 오류가 발생했습니다.');
        }
    });
});
