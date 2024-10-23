document.addEventListener('DOMContentLoaded', function() {
    const postsPerPage = 5;
    let currentPage = 1;

    async function fetchPosts() {
        const response = await fetch(`/board?page=${currentPage}`, {
            credentials: 'include' // 세션 쿠키 포함
        });
        
        if (!response.ok) {
            console.error(`Error: Received status ${response.status}`);
            throw new Error('Server responded with an error');
        }

        const html = await response.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');

        // Update the table body
        const newTbody = doc.querySelector('.tableset-table tbody');
        const oldTbody = document.querySelector('.tableset-table tbody');
        oldTbody.innerHTML = newTbody.innerHTML;

        // Update pagination
        const newPagination = doc.querySelector('.pagiset-list');
        const oldPagination = document.querySelector('.pagiset-list');
        oldPagination.innerHTML = newPagination.innerHTML;

        setupPaginationEvents();
    }

    function setupPaginationEvents() {
        const paginationLinks = document.querySelectorAll('.pagiset-link');
        paginationLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const page = parseInt(link.textContent);
                if (!isNaN(page)) {
                    currentPage = page;
                    fetchPosts();
                }
            });
        });
    }

    // Add event listener to "목록으로" button for going back
    const backButton = document.querySelector('.btnset.btnset-round.btnset-line.btnset-black');
    if (backButton) {
        backButton.addEventListener('click', (e) => {
            e.preventDefault();
            history.back(); // Go back to the previous page
        });
    }

    // Initial setup
    setupPaginationEvents();

    // Fetch posts only if it's not the initial server-side rendered page
    if (document.querySelector('.debug-info')) {
        console.log('Initial server-side rendered page');
    } else {
        fetchPosts();
    }
});