import React, { useState } from 'react'
import Header from './Head.jsx'
import './Head.css'
import './Anabada.css'
import arrow from './assets/free-icon-down-3444465.png'
import arrowTurn from './assets/icon.png'
import Footer from './Footer.jsx'
const Anabada = () => {
  const [showPopup, setShowPopup] = useState(false);

  const handleImageClick = () => {
    setShowPopup(true);
  };

  const handleClosePopup = () => {
    setShowPopup(false);
  };

  return (
    <>
        <Header/>
        <main>
          <div className='text-container'>
            <p className='text'>Today's new posts</p>
          </div>
          <div className='box-container'>
            <div className='box'>
              <div className='box-photoContainer'>
                <div className='box-photo' onClick={handleImageClick}><img src='#' alt='옷사진'></img></div>
              </div>
              <div className='nick-container'>
                <div className='profile-img'>
                  <img src='#' alt=''></img>
                </div>
                <p className='nick'>닉네임</p>
              </div>
            </div>
            {showPopup && (
              <div className='popup'>
                <div className='popup-content'>
                  <span className='close' onClick={handleClosePopup}>&times;</span>
                    <div className='popUp_imgBox'>
                      <div className='popUp_imgBox_img'><img src='#' alt='사진'></img></div>
                      <div className='arrow_container'><img src={arrow} className='right_arrow'></img></div>
                      <div className='arrow_container'><img src={arrowTurn} className='left_arrow'></img></div>
                    </div>
                      <div>
                        <div className='popUp_container'>
                          <div className='popUp_nick'>
                            <div className='profile-img'>
                              <img src='#' alt='프로필 이미지' />
                            </div>
                              <p>닉네임</p>
                          </div>
                          <div className='popUp_text'><p>내용</p></div>
                        </div>
                    </div>
                </div>
              </div>
      )}  
          </div>
        </main>
        <Footer/>
    </>
  )
}

export default Anabada