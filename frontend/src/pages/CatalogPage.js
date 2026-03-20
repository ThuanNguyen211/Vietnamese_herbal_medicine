import React, { useState, useEffect, useMemo } from 'react';
import { Link } from 'react-router-dom';
import { FaSearch, FaLeaf, FaArrowRight } from 'react-icons/fa';
import { API_BASE_URL, getCatalog, searchPlants } from '../services/api';
import './CatalogPage.css';

const INITIAL_VISIBLE_PLANTS = 10;
const DESKTOP_FEATURED_VISIBLE = 5;

const getFeaturedVisibleCount = (width) => {
  if (width <= 576) return 1;
  if (width <= 900) return 2;
  if (width <= 1200) return 3;
  return DESKTOP_FEATURED_VISIBLE;
};

const USAGE_GROUPS = [
  {
    key: 'thanh-nhiet',
    label: 'Thanh nhiệt - Giải độc',
    keywords: ['thanh nhiet', 'giai doc', 'mat gan', 'nong trong', 'giai nhiet'],
  },
  {
    key: 'ho-hap',
    label: 'Hô hấp - Ho - Viêm họng',
    keywords: ['ho', 'viem hong', 'dom', 'phe quan', 'hen', 'ho hap'],
  },
  {
    key: 'tieu-hoa',
    label: 'Tiêu hóa - Dạ dày',
    keywords: ['tieu hoa', 'da day', 'dau bung', 'tieu chay', 'dai trang', 'kiet ly'],
  },
  {
    key: 'da-lieu',
    label: 'Da liễu - Mụn - Ngứa',
    keywords: ['mun', 'da lieu', 'viem da', 'ngua', 'lo loet', 'di ung'],
  },
  {
    key: 'xuong-khop',
    label: 'Xương khớp - Phong thấp',
    keywords: ['xuong khop', 'phong thap', 'thap khop', 'dau nhuc', 'co xuong'],
  },
  {
    key: 'an-than',
    label: 'An thần - Giấc ngủ',
    keywords: ['an than', 'mat ngu', 'than kinh', 'stress', 'lo au'],
  },
];

const normalizeText = (text = '') =>
  text
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '');

function CatalogPage() {
  const [catalog, setCatalog] = useState([]);
  const [visiblePlantsCount, setVisiblePlantsCount] = useState(INITIAL_VISIBLE_PLANTS);
  const [featuredSlideIndex, setFeaturedSlideIndex] = useState(0);
  const [featuredVisibleCount, setFeaturedVisibleCount] = useState(() =>
    getFeaturedVisibleCount(window.innerWidth)
  );
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadCatalog();
  }, []);

  useEffect(() => {
    setVisiblePlantsCount(INITIAL_VISIBLE_PLANTS);
  }, [catalog]);

  useEffect(() => {
    const handleResize = () => {
      setFeaturedVisibleCount(getFeaturedVisibleCount(window.innerWidth));
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const loadCatalog = async () => {
    try {
      setLoading(true);
      const data = await getCatalog();
      setCatalog(data);
    } catch (err) {
      setError('Không thể tải danh mục. Vui lòng thử lại.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const allPlants = useMemo(
    () => catalog.flatMap((group) => group.plants || []),
    [catalog]
  );

  const featuredPlants = useMemo(() => allPlants.slice(0, 12), [allPlants]);
  const heroPlant = featuredPlants[0] || null;
  const visiblePlants = useMemo(
    () => allPlants.slice(0, visiblePlantsCount),
    [allPlants, visiblePlantsCount]
  );

  const featuredMaxIndex = useMemo(
    () => Math.max(0, featuredPlants.length - featuredVisibleCount),
    [featuredPlants.length, featuredVisibleCount]
  );

  useEffect(() => {
    setFeaturedSlideIndex(0);
  }, [featuredPlants.length, featuredVisibleCount]);

  useEffect(() => {
    if (featuredPlants.length <= featuredVisibleCount) {
      return undefined;
    }

    const autoplayTimer = setInterval(() => {
      setFeaturedSlideIndex((prev) => (prev >= featuredMaxIndex ? 0 : prev + 1));
    }, 2600);

    return () => clearInterval(autoplayTimer);
  }, [featuredPlants.length, featuredVisibleCount, featuredMaxIndex]);

  const groupedByUsage = useMemo(() => {
    const groups = USAGE_GROUPS.map((group) => ({
      key: group.key,
      label: group.label,
      plants: [],
    }));
    const otherGroup = {
      key: 'khac',
      label: 'Nhóm khác',
      plants: [],
    };

    allPlants.forEach((plant) => {
      const usageText = normalizeText(plant.usage || '');
      const matchedGroup = USAGE_GROUPS.find((group) =>
        group.keywords.some((keyword) => usageText.includes(keyword))
      );

      if (matchedGroup) {
        const target = groups.find((group) => group.key === matchedGroup.key);
        if (target) {
          target.plants.push(plant);
        }
      } else {
        otherGroup.plants.push(plant);
      }
    });

    return [...groups, otherGroup].filter((group) => group.plants.length > 0);
  }, [allPlants]);

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

  const handleShowMore = () => {
    setVisiblePlantsCount((prev) => prev + INITIAL_VISIBLE_PLANTS);
  };

  const renderPlantCard = (plant, compact = false) => (
    <Link
      key={plant.id}
      to={`/plant/${plant.id}`}
      className={`plant-card ${compact ? 'compact' : ''}`}
    >
      <div className="plant-thumb">
        {plant.image_url ? (
          <img src={`${API_BASE_URL}${plant.image_url}`} alt={plant.name} />
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
  );

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
          Vietnamese Herbal Atlas
        </h1>
        <p className="subtitle">Hệ thống truy vấn thông tin cây thuốc nam tại Việt Nam</p>
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
          <h3>Kết quả tìm kiếm: "{searchQuery}"</h3>
          {searchResults.length > 0 ? (
            <div className="search-grid">
              {searchResults.map((plant) => renderPlantCard(plant))}
            </div>
          ) : (
            <p className="no-results">Không tìm thấy kết quả nào.</p>
          )}
        </div>
      ) : (
        <div className="layout-option-two">
          {heroPlant && (
            <section className="hero-section">
              <div className="hero-content">
                <p className="hero-badge">Cây nổi bật hôm nay</p>
                <h2>{heroPlant.name}</h2>
                {heroPlant.scientific_name && (
                  <p className="hero-science">{heroPlant.scientific_name}</p>
                )}
                <Link to={`/plant/${heroPlant.id}`} className="hero-link">
                  Xem chi tiết <FaArrowRight />
                </Link>
              </div>
              <div className="hero-image-wrap">
                {heroPlant.image_url ? (
                  <img src={`${API_BASE_URL}${heroPlant.image_url}`} alt={heroPlant.name} />
                ) : (
                  <div className="hero-placeholder">
                    <FaLeaf />
                  </div>
                )}
              </div>
            </section>
          )}

          <section className="featured-slider-section">
            <div className="section-heading">
              <h2>Cây thuốc nổi bật</h2>
            </div>
            <div className="featured-carousel">
              <div className="carousel-viewport">
                <div
                  className="carousel-track"
                  style={{
                    transform: `translateX(-${(100 / featuredVisibleCount) * featuredSlideIndex}%)`,
                  }}
                >
                  {featuredPlants.map((plant) => (
                    <div
                      key={plant.id}
                      className="carousel-slide"
                      style={{
                        flex: `0 0 ${100 / featuredVisibleCount}%`,
                        minWidth: `${100 / featuredVisibleCount}%`,
                      }}
                    >
                      {renderPlantCard(plant, true)}
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {featuredPlants.length === 0 && (
              <p className="no-results">Chưa có dữ liệu cây nổi bật.</p>
            )}
          </section>

          <section className="explore-grid-section">
            <div className="section-heading">
              <h2>Khám phá toàn bộ danh mục</h2>
            </div>
            <div className="plant-grid">
              {visiblePlants.map((plant) => renderPlantCard(plant))}
            </div>
            {visiblePlantsCount < allPlants.length && (
              <div className="show-more-wrap">
                <button className="show-more-btn" onClick={handleShowMore}>
                  Xem thêm
                </button>
              </div>
            )}
          </section>

          {/* <section className="grouped-usage-tail">
            <div className="section-heading">
              <h2>Nhóm theo danh mục công dụng</h2>
            </div>
            <div className="layout-option-three">
              <p className="group-intro">
                Danh mục được gom theo công dụng phổ biến để bạn tìm cây nhanh hơn theo nhu cầu điều trị.
              </p>
              {groupedByUsage.map((group) => (
                <section key={group.key} className="usage-section">
                  <div className="section-heading">
                    <h2>{group.label}</h2>
                  </div>
                  <div className="plant-grid">
                    {group.plants.slice(0, 8).map((plant) => renderPlantCard(plant))}
                  </div>
                </section>
              ))}
            </div>
          </section> */}
        </div>
      )}
    </div>
  );
}

export default CatalogPage;
