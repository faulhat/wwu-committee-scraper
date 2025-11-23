// src/App.jsx
import React, { useState, useEffect, useMemo } from 'react';
import CommitteeList from '../CommitteeList/CommitteeList';
import Footer from '../Footer/Footer';
import Subheader from '../Subheader/Subheader';
import { Toaster } from 'react-hot-toast';
import './App.css';
import gif from '../../assets/oldmain.gif';
import img2 from '../../assets/wwuheader.png';
import img3 from '../../assets/mywestern.png';
//import img4 from '../../assets/a.png';
import img5 from '../../assets/apply.png';
import img6 from '../../assets/give.png';

function App() {
  const [committees, setCommittees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [visibleCount, setVisibleCount] = useState(6);
  const [searchTerm, setSearchTerm] = useState('');

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

  const filteredCommittees = useMemo(() => {
    if (!searchTerm.trim()) {
      return committees;
    }

    const lowerSearchTerm = searchTerm.toLowerCase();
    
    return committees.filter(committee => {
      const title = committee.title?.toLowerCase() || '';
      const url = committee.url?.toLowerCase() || '';
      const summaryBefore = committee.summary_before?.toLowerCase() || '';
      const summaryKeyword = committee.summary_keyword?.toLowerCase() || '';
      const summaryAfter = committee.summary_after?.toLowerCase() || '';
      let subdomain = '';
      try {
        const urlObject = new URL(committee.url);
        const hostname = urlObject.hostname;
        const parts = hostname.split('.');
        if (parts.length >= 3) {
          subdomain = parts.slice(0, -2).join('.').toLowerCase();
        }
      } catch (error) {
        console.log("error subdomain search");
      }
      return (
        title.includes(lowerSearchTerm) ||
        url.includes(lowerSearchTerm) ||
        summaryBefore.includes(lowerSearchTerm) ||
        summaryKeyword.includes(lowerSearchTerm) ||
        summaryAfter.includes(lowerSearchTerm) ||
        subdomain.includes(lowerSearchTerm)
      );
    });
  }, [committees, searchTerm]);

  const handleLoadMore = () => {
    setVisibleCount(prev => prev + 10);
  };

  useEffect(() => {
    setVisibleCount(10);
  }, [searchTerm]);

  const visibleCommittees = filteredCommittees.slice(0, visibleCount);

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
        </div>
      </h1>
      <Subheader />
      <div className="image-container">
        <img src={gif} alt="Western Washington University" className="gif" />
      </div>
      <h2 className="committee-main-title">WWU Student Committees</h2>
      
      {loading ? (
        <div className="loading-message">Loading committees...</div>
      ) : (
        <>
          <div className="search-container">
            <input
              type="text"
              placeholder="Search all committees by name, subdomain, or content..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="search-input"
            />
          </div>
          {searchTerm && (
            <div className="search-results-info">
              Found {filteredCommittees.length} committee{filteredCommittees.length !== 1 ? 's' : ''} 
              {filteredCommittees.length > 0 && ` (showing ${visibleCommittees.length})`}
            </div>
          )}
          <CommitteeList committees={visibleCommittees} />
          {visibleCount < filteredCommittees.length && (
            <div className="load-more-container">
              <button
                className="load-more-button"
                onClick={handleLoadMore}>
                Load (10) More ({filteredCommittees.length - visibleCount} remaining)
              </button>
            </div>
          )}
          {visibleCommittees.length === 0 && searchTerm && (
            <div className="no-results-message">
              No committees found matching "{searchTerm}"
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
