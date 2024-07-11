import React from 'react';
import logo from './assets/logo.PNG'; // 이미지 파일 경로
import li from './assets/Person.jpg';
import './Head.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const Head = () => {
  return (
    <header className="header">
      <div className="logoContainer">
        <img src={logo} alt="logo" className="logo" />
      </div>
      <div className="myRoomContainer">
        <div className="myRoom">
          <div className="myRoom_iconLine">
            <img src={li} alt="profile" style={{ width: 25, height: 25, marginTop: 2 }} />
          </div>
          <div className="myRoomContext">
            <a href="#Profile">
              <p>Profile</p>
            </a>
          </div>
        </div>
      </div>
      <div className="nav_list">
        <nav className="nav">
          <ul>
            <li>Swit</li>
            <li>Anabada</li>
            <li>Clothing bin</li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Head;
