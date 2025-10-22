// src/App.jsx
import React, { useState, useEffect } from 'react';
import CommitteeList from '../CommitteeList/CommitteeList';
import Footer from '../Footer/Footer';
import Subheader from '../Subheader/Subheader';
import { Toaster } from 'react-hot-toast';
import './App.css';
import gif from '../../assets/oldmain.gif';
import img2 from '../../assets/img2.png';
import img3 from '../../assets/aa.png';
import img4 from '../../assets/a.png';
import img5 from '../../assets/aaa.png';
import img6 from '../../assets/aaaa.png';

function App() {
  const [committees, setCommittees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [visibleCount, setVisibleCount] = useState(6);

  useEffect(() => {
    const fetchCommittees = async () => {
      try {
        const res = await fetch('/pages.json');
        const data = await res.json();
        setCommittees(data);
      } catch (error) {
        console.error('Error fetching committees:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCommittees();
  }, []);

  const handleLoadMore = () => {
    setVisibleCount(prev => prev + 10);
  };

  return (
    <div className="App">
      <h1>
        <img src={img2} alt="WWU Logo" className="header-logo" />
        <div className="header-right-images">
          <a href="https://admissions.wwu.edu/apply" target="_blank" rel="noopener noreferrer">
            <img src={img5} alt="Apply Icon" className="header-icon" />
          </a>
          <a href="https://alumniq.wwu.edu/giving/make-a-gift" target="_blank" rel="noopener noreferrer">
            <img src={img6} alt="Donate Icon" className="header-icon" />
          </a>
          <a href="https://mywestern.wwu.edu/" target="_blank" rel="noopener noreferrer">
            <img src={img3} alt="MyWestern Icon" className="header-icon" />
          </a>
          <a href="https://search.wwu.edu/?q=%20site%3Amywestern.wwu.edu" target="_blank" rel="noopener noreferrer">
            <img src={img4} alt="Search Icon" className="header-icon" />
          </a>
        </div>
      </h1>

      <Subheader />

      <div className="image-container">
        <img src={gif} alt="Western Washington University" className="gif" />
      </div>

      <h2 className="committee-main-title">WWU Student Committees
      </h2>
      
      {loading ? (
        <div className="loading-message">Loading committees...</div>
      ) : (
        <>
          <CommitteeList committees={committees.slice(0, visibleCount)} />

          {visibleCount < committees.length && (
            <div className="load-more-container">
              <button
                className="load-more-button"
                onClick={handleLoadMore}>
                Load More
              </button>
            </div>
          )}
        </>
      )}

      <Toaster position="top-center" reverseOrder={false} />
      <Footer />
    </div>
  );
}

export default App;
