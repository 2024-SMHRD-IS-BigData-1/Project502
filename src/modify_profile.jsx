import React, { useState } from 'react';
import './modify_profile.css';
import './Head.css'
import Header from './Head.jsx'
import 'bootstrap/dist/css/bootstrap.min.css';
import Footer from './Footer.jsx'; // Footer 추가 


function ModifyProfile() {
    const [photo, setPhoto] = useState(null);
    const [nickname, setNickname] = useState('');
    const [introduce, setIntroduce] = useState('');

    const handlePhotoChange = (e) => {
        setPhoto(e.target.files[0]);
    };

    const handleNicknameChange = (e) => {
        setNickname(e.target.value);
    };

    const handleIntroduceChange = (e) => {
        setIntroduce(e.target.value);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log('Photo:', photo);
        console.log('Nickname:', nickname);
        console.log('Introduce:', introduce);
        // 여기에 API 호출 또는 상태 업데이트 로직 추가 가능
    };

    return (
        <>
        <Header/>
        <div className="modify-profile-container">
            
            <form onSubmit={handleSubmit} className="modify-profile-form">
                <div className="form-group">
                <h4 className="pageName">Modify My Profile</h4><br/><br/>
                    <label htmlFor="photo">Photo</label>
                    <input
                        type="file"
                        id="photo"
                        onChange={handlePhotoChange}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="nickname">Nickname</label>
                    <input
                        type="text"
                        id="nickname"
                        value={nickname}
                        onChange={handleNicknameChange}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="introduce">Introduce</label>
                    <textarea
                        id="introduce"
                        value={introduce}
                        onChange={handleIntroduceChange}
                        required
                    />
                </div>
                <button type="submit" className="modify-button">수정</button>
            </form>
        </div>
        <Footer /> {/* Footer 추가 */}
        </>
    );
}

export default ModifyProfile;
