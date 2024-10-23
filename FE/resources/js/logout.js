// 로그아웃
document.getElementById("logoutButton").addEventListener("click", function() {
    fetch('/logout', {
        method: 'POST',
        credentials: 'include' // 세션 쿠키 포함
    })
    .then(response => {
        if (response.ok) {
            alert("로그아웃되었습니다.");
            window.location.href = "/login";
        } else {
            throw new Error("로그아웃 처리 중 오류가 발생했습니다.");
        }
    })
    .catch(error => {
        console.error('Logout error:', error);
        alert(error.message);
    });
});