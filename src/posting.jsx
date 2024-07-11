import React, { useState, useRef } from 'react';
import './Posting.css';
import './Head.css';
import Header from './Head.jsx';
import 'bootstrap/dist/css/bootstrap.min.css';
import Footer from './Footer.jsx'; // Footer 추가 

function Posting() {
    const [title, setTitle] = useState('');
    const [category, setCategory] = useState('교환');
    const [images, setImages] = useState(null);
    const [content, setContent] = useState('');

    const fileInputRef = useRef(null);

    const handleTitleChange = (e) => {
        setTitle(e.target.value);
    };

    const handleCategoryChange = (e) => {
        setCategory(e.target.value);
    };

    const handleImagesChange = (e) => {
        setImages(e.target.files);
    };

    const handleContentChange = (e) => {
        setContent(e.target.value);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log('Title:', title);
        console.log('Category:', category);
        console.log('Images:', images);
        console.log('Content:', content);
        // 여기에 API 호출 또는 상태 업데이트 로직 추가 가능
    };

    const handleImageUploadClick = () => {
        fileInputRef.current.click();
    };

    return (
        <>
            <Header />
            <div className="posting-container">
                <form onSubmit={handleSubmit} className="posting-form">
                    <div className="form-group text-center">
                        <h4 className="pageName">Write a Post</h4><br/><br/>
                    </div>
                    <div className="form-group" style={{ textAlign: 'center' }}>
                        <label htmlFor="title">Title</label>
                        <input
                            type="text"
                            id="title"
                            value={title}
                            onChange={handleTitleChange}
                            required
                        />
                    </div>
                    <div className="form-group" style={{ textAlign: 'center' }}>
                        <label htmlFor="category">Category</label>
                        <select
                            id="category"
                            value={category}
                            onChange={handleCategoryChange}
                            required
                        >
                            <option value="교환">교환</option>
                            <option value="구매">구매</option>
                        </select>
                    </div>
                    <div className="form-group" style={{ textAlign: 'center' }}>
                        <label htmlFor="images">Images</label>
                        <button
                            type="button"
                            className="image-upload-button"
                            onClick={handleImageUploadClick}
                        >
                            Upload Images
                        </button>
                        <input
                            type="file"
                            id="images"
                            multiple
                            onChange={handleImagesChange}
                            ref={fileInputRef}
                            style={{ display: 'none' }}
                        />
                    </div>
                    <div className="form-group" style={{ textAlign: 'center' }}>
                        <label htmlFor="content">Content</label>
                        <textarea
                            id="content"
                            value={content}
                            onChange={handleContentChange}
                            required
                        />
                    </div>
                    <button type="submit" className="upload-button">Upload</button>
                </form>
            </div>
            <Footer /> {/* Footer 추가 */}
        </>
    );
}

export default Posting;
