document.addEventListener('DOMContentLoaded', function() {
    console.log('Post page loaded');
    console.log('Post title:', document.querySelector('.textset-tit').textContent);
    console.log('Post author and date:', document.querySelector('.textset-sub p').textContent);
    console.log('Post content:', document.querySelector('.contents-body').innerHTML);

    const editButton = document.querySelector('.btnset-round.btnset-line:nth-child(2)');
    if (editButton) {
        editButton.addEventListener('click', function(e) {
            e.preventDefault();
            const postId = window.location.pathname.split('/').pop();
            window.location.href = `/boardupdate/${postId}`;
        });
    }
});

