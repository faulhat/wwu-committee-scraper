import React from 'react';
import './Footer.css';
import img from '../../assets/img.png';

function Footer() {
  const handleExport = () => {
    window.location.href = '/pages.xlsx';
  };

  return (
    <footer className="footer">
      {/* Top level: original navigation */}
      <div className="footer-content">
        <a
          href="https://as.wwu.edu/gov/contacts/"
          className="footer-link"
          target="_blank"
          rel="noopener noreferrer"
        >
          CONTACT
        </a>

        <a
          href="https://hr.wwu.edu/work-western"
          className="footer-link"
          target="_blank"
          rel="noopener noreferrer"
        >
          JOBS
        </a>

        <a
          href="https://vu.wwu.edu/policies"
          className="footer-link"
          target="_blank"
          rel="noopener noreferrer"
        >
          FEES & POLICIES
        </a>

        <a
          href="https://www.wwu.edu/online-privacy-statement"
          className="footer-link"
          target="_blank"
          rel="noopener noreferrer"
        >
          PRIVACY
        </a>

        <a
          href="https://www.wwu.edu/commitment-accessibility"
          className="footer-link"
          target="_blank"
          rel="noopener noreferrer"
        >
          ACCESSIBILITY
        </a>
      </div>

      {/* Second level: export */}
      <div className="footer-export">
        <button
          className="footer-link footer-export-link"
          onClick={handleExport}
        >
          EXPORT TO EXCEL
        </button>
      </div>

      {/* Image */}
      <div className="footer-image-container">
        <img src={img} alt="Footer Image" className="footer-image" />
      </div>
    </footer>
  );
}

export default Footer;
