document.getElementById('signup-btn').addEventListener('click', async () => {
    // 입력값 가져오기
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const email = document.getElementById('email').value;
    const country = document.getElementById('country').value;
    const privacyAgree = document.getElementById('privacy-agree').checked;

    // 개인정보 동의 확인
    if (!privacyAgree) {
      alert('개인정보 수집 및 이용에 동의해야 합니다.');
      return;
    }

    // 서버로 보낼 데이터
    const data = {
      username: username,
      password: password,
      email: email,
      country: country
    };

    try {
      // POST 요청으로 회원가입 처리
      const response = await fetch('/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      // 응답 처리
      if (response.ok) {
        alert('회원가입이 성공적으로 완료되었습니다.');
        window.location.href = '/signup_complete';
      } else if (response.status === 400) {
        // 서버에서 400 에러를 반환한 경우 (아이디 또는 이메일 중복)
        const errorData = await response.json();
        if (errorData.detail === '이미 존재하는 사용자 이름입니다.') {
          alert('이미 존재하는 사용자 이름입니다. 다른 아이디를 사용해주세요.');
        } else if (errorData.detail === '이미 존재하는 이메일입니다.') {
          alert('이미 존재하는 이메일입니다. 다른 이메일을 사용해주세요.');
        } else {
          alert('회원가입에 실패했습니다. 다시 시도해 주세요.');
        }
      } else {
        alert('회원가입에 실패했습니다. 다시 시도해 주세요.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('서버 오류가 발생했습니다.');
    }
  });
