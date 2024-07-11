import React, { useState } from 'react';
import './Login.css';
import logo from './assets/logo.PNG';
import 'bootstrap/dist/css/bootstrap.min.css';
import Footer from './Footer.jsx'; // Footer 추가 



function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleEmailChange = (e) => {
        setEmail(e.target.value);
    };

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        // 여기에 로그인 로직을 추가하세요.
        console.log('Email:', email);
        console.log('Password:', password);
    };

    return (
        <>
        <div className="login-container">
            <form onSubmit={handleSubmit} className="login-form">
                <img src={logo} alt="Logo" className="login-logo" /> {/* 로고 이미지 추가 */}
                <div className="form-group">
                    <input
                        type="email"
                        id="email"
                        value={email}
                        onChange={handleEmailChange}
                        placeholder="ID를 입력해주세요." /* placeholder 추가 */
                        required
                    />
                </div>
                <div className="form-group">
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={handlePasswordChange}
                        placeholder="PW를 입력해주세요." /* placeholder 추가 */
                        required
                    />
                </div>
                <button type="submit" className="login-button">Login</button>
                <a href="join.jsx" className="signup-link">회원가입</a> {/* 회원가입 링크 추가 */}
            </form>
        </div>
        <Footer /> {/* Footer 추가 */}
        </>
    );
}

export default Login;
