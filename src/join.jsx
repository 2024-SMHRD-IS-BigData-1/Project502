import React, { useState } from 'react';
import './Join.css';
import logo from './assets/logo.PNG';
import 'bootstrap/dist/css/bootstrap.min.css';
import Footer from './Footer.jsx'; // Footer 추가 


function Join() {
    const [userId, setUserId] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [nickname, setNickname] = useState('');
    const [email, setEmail] = useState('');
    const [gender, setGender] = useState('');
    const [phoneNumber, setPhoneNumber] = useState('');
    const [verificationCode, setVerificationCode] = useState('');

    const handleUserIdChange = (e) => {
        setUserId(e.target.value);
    };

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    };

    const handleConfirmPasswordChange = (e) => {
        setConfirmPassword(e.target.value);
    };

    const handleNicknameChange = (e) => {
        setNickname(e.target.value);
    };

    const handleEmailChange = (e) => {
        setEmail(e.target.value);
    };

    const handleGenderChange = (value) => {
        setGender(value);
    };

    const handlePhoneNumberChange = (e) => {
        setPhoneNumber(e.target.value);
    };

    const handleVerificationCodeChange = (e) => {
        setVerificationCode(e.target.value);
    };

    const handleVerification = () => {
        console.log('Verification logic goes here');
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log('User ID:', userId);
        console.log('Password:', password);
        console.log('Confirm Password:', confirmPassword);
        console.log('Nickname:', nickname);
        console.log('Email:', email);
        console.log('Gender:', gender);
        console.log('Phone Number:', phoneNumber);
        console.log('Verification Code:', verificationCode);
    };

    return (
        <>
        <div className="join-container">
            <form onSubmit={handleSubmit} className="join-form">
                <img src={logo} alt="Logo" className="join-logo" />
                <div className="form-group">
                    <label htmlFor="userId">아이디</label>
                    <input
                        type="text"
                        id="userId"
                        value={userId}
                        onChange={handleUserIdChange}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="password">비밀번호</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={handlePasswordChange}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="confirmPassword">비밀번호 확인</label>
                    <input
                        type="password"
                        id="confirmPassword"
                        value={confirmPassword}
                        onChange={handleConfirmPasswordChange}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="nickname">닉네임</label>
                    <input
                        type="text"
                        id="nickname"
                        value={nickname}
                        onChange={handleNicknameChange}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="email">E-Mail</label>
                    <input
                        type="email"
                        id="email"
                        value={email}
                        onChange={handleEmailChange}
                        required
                    />
                </div>
                <div className="form-group">
                    <label>성별</label>
                    <div className="gender-group">
                        <label>
                            <input
                                type="radio"
                                name="gender"
                                value="male"
                                checked={gender === 'male'}
                                onChange={() => handleGenderChange('male')}
                            /> 남성
                        </label>
                        <label>
                            <input
                                type="radio"
                                name="gender"
                                value="female"
                                checked={gender === 'female'}
                                onChange={() => handleGenderChange('female')}
                            /> 여성
                        </label>
                    </div>
                </div>
                <div className="form-group">
                    <label htmlFor="phoneNumber">전화번호</label>
                    <div className="phone-input-group">
                        <input
                            type="text"
                            id="phoneNumber"
                            value={phoneNumber}
                            onChange={handlePhoneNumberChange}
                            required
                            style={{ width: 'calc(100% - 100px)' }}
                        />
                        <button type="button" className="verification-button" onClick={handleVerification}>
                            인증
                        </button>
                    </div>
                </div>
                <div className="form-group">
                    <label htmlFor="verificationCode">인증 코드</label>
                    <input
                        type="text"
                        id="verificationCode"
                        value={verificationCode}
                        onChange={handleVerificationCodeChange}
                        required
                    />
                </div>
                <button type="submit" className="join-button">Join</button>
            </form>
        </div>
        <Footer /> {/* Footer 추가 */}
        </>
    );
}

export default Join;
