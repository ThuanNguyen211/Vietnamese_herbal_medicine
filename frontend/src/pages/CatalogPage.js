import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FaChevronDown, FaChevronUp, FaSearch, FaLeaf } from 'react-icons/fa';
import { getCatalog, searchPlants } from '../services/api';
import './CatalogPage.css';

function CatalogPage() {
  const [catalog, setCatalog] = useState([]);
  const [expandedLetters, setExpandedLetters] = useState({});
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadCatalog();
  }, []);

  const loadCatalog = async () => {
    try {
      setLoading(true);
      const data = await getCatalog();
      setCatalog(data);
      // Mở rộng chữ cái đầu tiên mặc định
      if (data.length > 0) {
        setExpandedLetters({ [data[0].letter]: true });
      }
    } catch (err) {
      setError('Không thể tải danh mục. Vui lòng thử lại.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const toggleLetter = (letter) => {
    setExpandedLetters((prev) => ({
      ...prev,
      [letter]: !prev[letter],
    }));
  };

  const handleSearch = async (e) => {
    const query = e.target.value;
    setSearchQuery(query);

    if (query.trim().length >= 2) {
      try {
        const results = await searchPlants(query.trim());
        setSearchResults(results);
      } catch (err) {
        console.error(err);
      }
    } else {
      setSearchResults(null);
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <FaLeaf className="loading-icon spin" />
        <p>Đang tải danh mục...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <p>{error}</p>
        <button onClick={loadCatalog} className="retry-btn">Thử lại</button>
      </div>
    );
  }

  return (
    <div className="catalog-page">
      <div className="catalog-header">
        <h1>
          <FaLeaf className="header-icon" />
          Vietnamese herbal medicine
        </h1>
        <p className="subtitle">Danh mục cây thuốc nam Việt Nam</p>
      </div>

      {/* Search bar */}
      <div className="search-bar">
        <FaSearch className="search-icon" />
        <input
          type="text"
          placeholder="Tìm kiếm cây thuốc nam..."
          value={searchQuery}
          onChange={handleSearch}
        />
      </div>

      {/* Search results */}
      {searchResults !== null ? (
        <div className="search-results">
          <h3>Kết quả tìm kiếm: "{searchQuery}" ({searchResults.length} kết quả)</h3>
          {searchResults.length > 0 ? (
            <div className="plant-list">
              {searchResults.map((plant) => (
                <Link key={plant.id} to={`/plant/${plant.id}`} className="plant-item">
                  <div className="plant-thumb">
                    {plant.image_url ? (
                      <img src={`http://localhost:8000${plant.image_url}`} alt={plant.name} />
                    ) : (
                      <FaLeaf className="plant-placeholder-icon" />
                    )}
                  </div>
                  <div className="plant-info">
                    <span className="plant-name">{plant.name}</span>
                    {plant.scientific_name && (
                      <span className="plant-scientific">{plant.scientific_name}</span>
                    )}
                  </div>
                </Link>
              ))}
            </div>
          ) : (
            <p className="no-results">Không tìm thấy kết quả nào.</p>
          )}
        </div>
      ) : (
        /* Accordion catalog */
        <div className="catalog-accordion">
          {catalog.map((group) => (
            <div key={group.letter} className="letter-group">
              <button
                className={`letter-header ${expandedLetters[group.letter] ? 'expanded' : ''}`}
                onClick={() => toggleLetter(group.letter)}
              >
                <span className="letter-title">{group.letter}</span>
                <span className="letter-count">{group.plants.length} cây</span>
                {expandedLetters[group.letter] ? (
                  <FaChevronUp className="chevron" />
                ) : (
                  <FaChevronDown className="chevron" />
                )}
              </button>
              {expandedLetters[group.letter] && (
                <div className="letter-content">
                  {group.plants.map((plant) => (
                    <Link key={plant.id} to={`/plant/${plant.id}`} className="plant-item">
                      <div className="plant-thumb">
                        {plant.image_url ? (
                          <img src={`http://localhost:8000${plant.image_url}`} alt={plant.name} />
                        ) : (
                          <FaLeaf className="plant-placeholder-icon" />
                        )}
                      </div>
                      <div className="plant-info">
                        <span className="plant-name">{plant.name}</span>
                        {plant.scientific_name && (
                          <span className="plant-scientific">{plant.scientific_name}</span>
                        )}
                      </div>
                    </Link>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default CatalogPage;
