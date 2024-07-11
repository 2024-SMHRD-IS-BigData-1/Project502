import React, { useState } from 'react';
import './Profile.css';
import './Head.css';
import Header from './Head.jsx';
import Footer from './Footer.jsx';
import 'bootstrap/dist/css/bootstrap.min.css';
import plus from './assets/add_13652631.png';
import dot from './assets/options.png';

const Profile = () => {
  const [postSpaces, setPostSpaces] = useState([]); // 사진이 들어갈 박스 여러 개 생성시키는 코드

  const handlePlusClick = () => {
    setPostSpaces([...postSpaces, {}]);
  };

  return (
    <>
      <Header />
      <div className="profile-container">
        <form className="profile-form">
          <div className="profile_picture_container">
            <div className="profile_picture">
              <img src="#" alt="profile" className="profile-img"></img>
            </div>
          </div>
         
          <div className="nick_container">
            <div className="nick"><h6><strong>닉네임</strong></h6></div>
          </div>
          <div className="intro_container">
            <div className="intro_mySelf"><h6>자기소개</h6></div>
          </div>
          <div className="dot-container">
            <div className="dot-img">
              <img src={dot} alt="options"></img>
            </div>
          </div>
          <div className="button-container">
            <button type="button" className="button">Chat</button>
          </div>
          <div className="plus-container">
            <button className="plus-button" onClick={handlePlusClick}>
              <img src={plus} alt="add post" className="plus_img"></img>
            </button>
          </div>
          <div className="post-container">
             
            
          </div>
        </form>
      </div>
      <Footer />
    </>
  );
};

export default Profile;
