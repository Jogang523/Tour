// 로그인 처리 함수
function submitLoginForm(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = {
        username: formData.get('username'),
        password: formData.get('password')
    };
    
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
        credentials: 'include' // 세션 쿠키 포함
    })
    .then(response => response.json().then(body => ({ status: response.status, body: body })))
    .then(result => {
        if (result.status === 200) {
            alert("로그인 성공!");
            window.location.href = '/';
        } else {
            throw new Error(result.body.detail || '로그인을 실패했습니다.');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        alert(error.message);
    });
}

// 마이페이지 접근 함수
function accessMypage() {
    fetch('/mypage', {
        method: 'GET',
        credentials: 'include' // 세션 쿠키 포함
    })
    .then(response => {
        if (response.status === 200) {
            return response.text();
        } else if (response.status === 401) {
            throw new Error('회원 인증에 실패했습니다. 로그인 페이지로 이동합니다.');
        } else {
            throw new Error('페이지 로드 중 오류가 발생했습니다.');
        }
    })
    .then(data => {
        document.body.innerHTML = data;
    })
    .catch(error => {
        console.error('Error:', error);
        alert(error.message);
        window.location.href = '/login';
    });
}

// 프로필 버튼 클릭 시 마이페이지로 이동
document.querySelector('.btn-profile').addEventListener('click', function(event) {
    event.preventDefault();
    accessMypage();
});

// 페이지 로드 시 로그인 상태 확인
fetch('/check-auth', {
    method: 'GET',
    credentials: 'include'
})
.then(response => response.json())
.then(data => {
    if (data.authenticated) {
        document.querySelector('.btn-profile').setAttribute('href', '/mypage');
    } else {
        document.querySelector('.btn-profile').setAttribute('href', '/login');
    }
})
.catch(error => {
    console.error('Error checking auth status:', error);
});