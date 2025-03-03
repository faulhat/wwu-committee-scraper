import React from 'react';
import './Footer.css';
import img from '../../assets/img.png'; // Import the image

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <a href="https://as.wwu.edu/gov/contacts/" className="footer-link" target="_blank">CONTACT</a>
        <a href="https://hr.wwu.edu/work-western" className="footer-link" target="_blank">JOBS</a>
        <a href="https://vu.wwu.edu/policies" className="footer-link" target="_blank">FEES & POLICIES</a>
        <a href="https://www.wwu.edu/online-privacy-statement" className="footer-link" target="_blank">PRIVACY</a>
        <a href="https://www.wwu.edu/commitment-accessibility" className="footer-link" target="_blank">ACCESSIBILITY</a>
      </div>
      {/* Add the image here */}
      <div className="footer-image-container">
        <img src={img} alt="Footer Image" className="footer-image" />
      </div>
    </footer>
  );
}

export default Footer;