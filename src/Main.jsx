import React from 'react'
import Header from './Head.jsx'
import './Main.css'
import photo from './assets/pexels-kseniachernaya-3965545.jpg'
import Footer from './Footer.jsx'

const Main = () => {
  return (
    
      <div className='main-container'>
          <Header/>
          <main>
            <div className='image-container'>
                <img src={photo} alt='사진' className='image'></img>
            </div>
            <div>
                <p className='under_text'>Find your outfit for today</p>
            </div>
          </main>
          <Footer/>
      </div>
    
  )
}

export default Main