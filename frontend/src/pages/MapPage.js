import React, { useMemo, useRef, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaImage, FaMapMarkedAlt, FaSearch, FaTimes, FaLeaf } from 'react-icons/fa';
import { sendMapMessage } from '../services/api';
import DistributionMap from '../components/DistributionMap';
import './MapPage.css';

function MapPage() {
  const navigate = useNavigate();
  const [inputText, setInputText] = useState('');
  const [selectedImage, setSelectedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [recommendedPlants, setRecommendedPlants] = useState([]);
  const [searchSummary, setSearchSummary] = useState('');
  const [error, setError] = useState('');
  const fileInputRef = useRef(null);

  // Load previous search results from sessionStorage on mount
  useEffect(() => {
    const savedState = sessionStorage.getItem('mapSearchState');
    if (savedState) {
      try {
        const { recommendedPlants: saved, searchSummary: savedSummary, sessionId: savedSessionId } = JSON.parse(savedState);
        setRecommendedPlants(saved || []);
        setSearchSummary(savedSummary || '');
        setSessionId(savedSessionId || null);
      } catch (e) {
        console.error('Failed to restore search state:', e);
      }
    }
  }, []);

  // Save search results to sessionStorage whenever they change
  useEffect(() => {
    if (recommendedPlants.length > 0 || searchSummary) {
      sessionStorage.setItem(
        'mapSearchState',
        JSON.stringify({
          recommendedPlants,
          searchSummary,
          sessionId,
        })
      );
    }
  }, [recommendedPlants, searchSummary, sessionId]);

  const mapCoords = useMemo(() => {
    const points = [];

    recommendedPlants.forEach((plant) => {
      const coords = Array.isArray(plant.distribution_coords) ? plant.distribution_coords : [];
      coords.forEach((coord) => {
        const lat = Number(coord.lat);
        const lng = Number(coord.lng);

        if (!Number.isFinite(lat) || !Number.isFinite(lng)) {
          return;
        }

        points.push({
          lat,
          lng,
          location: coord.location || 'Khu vực chưa rõ tên',
          plantName: plant.name,
          scientificName: plant.scientific_name,
          usage: plant.usage,
          confidence: plant.confidence,
        });
      });
    });

    return points;
  }, [recommendedPlants]);

  const handleImageSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onload = (ev) => setImagePreview(ev.target.result);
      reader.readAsDataURL(file);
    }
  };

  const removeImage = () => {
    setSelectedImage(null);
    setImagePreview(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const handleSearch = async (e) => {
    e.preventDefault();

    if (!inputText.trim() && !selectedImage) return;

    const msgText = inputText.trim();
    const msgImage = selectedImage;

    setLoading(true);
    setError('');

    try {
      const response = await sendMapMessage({
        message: msgText || null,
        image: msgImage,
        sessionId,
      });

      setSessionId(response.session_id);
      setRecommendedPlants(Array.isArray(response.recommended_plants) ? response.recommended_plants : []);
      setSearchSummary(response.reply || '');
      setInputText('');
      removeImage();

      if (!response.recommended_plants || response.recommended_plants.length === 0) {
        setError('Không tìm thấy kết quả phù hợp. Bạn có thể thử mô tả chi tiết hơn.');
      }
    } catch (err) {
      console.error(err);
      setError('Xin lỗi, đã có lỗi khi tìm kiếm. Vui lòng thử lại.');
    } finally {
      setLoading(false);
    }
  };

  const cleanedSummary = useMemo(() => {
    return (searchSummary || '').replace(/\*\*/g, '').replace(/[📷🌿]/g, '').trim();
  }, [searchSummary]);

  return (
    <div className="map-search-page">
      <form className="map-search-form" onSubmit={handleSearch}>
        <div className="search-input-wrapper">
          {/* <FaSearch className="search-icon" /> */}
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Nhập tên cây, mô tả đặc điểm, công dụng hoặc triệu chứng..."
            disabled={loading}
          />
        </div>

        <input
          type="file"
          accept="image/*"
          ref={fileInputRef}
          onChange={handleImageSelect}
          style={{ display: 'none' }}
        />

        <button
          type="button"
          className="image-btn"
          onClick={() => fileInputRef.current?.click()}
          disabled={loading}
        >
          <FaImage />
          Tải ảnh
        </button>

        <button
          type="submit"
          className="search-btn"
          disabled={loading || (!inputText.trim() && !selectedImage)}
        >
          <FaMapMarkedAlt />
          {loading ? 'Đang tìm...' : 'Tìm trên bản đồ'}
        </button>
      </form>

      {imagePreview && (
        <div className="image-preview-chip">
          <img src={imagePreview} alt="Uploaded preview" />
          <span>Ảnh tìm kiếm đã được chọn</span>
          <button onClick={removeImage} className="remove-image-btn" type="button" aria-label="Xóa ảnh">
            <FaTimes />
          </button>
        </div>
      )}

      {error && <p className="search-error">{error}</p>}
      {!error && cleanedSummary && <p className="search-summary">{cleanedSummary}</p>}

      <div className="search-map-wrap">
        <DistributionMap
          coords={mapCoords}
          plantName={recommendedPlants.length > 0 ? 'kết quả tìm kiếm' : 'khu vực mặc định'}
          height="100%"
          legendLabel="Vị trí tìm thấy"
        />
      </div>

      <div className="search-results-grid">
        {recommendedPlants.length === 0 && !loading && (
          <div className="empty-result-card">
            <FaLeaf />
            <p>Chưa có kết quả. Hãy nhập mô tả hoặc tải ảnh để bắt đầu tìm kiếm.</p>
          </div>
        )}

        {recommendedPlants.map((plant) => {
          const pointCount = Array.isArray(plant.distribution_coords) ? plant.distribution_coords.length : 0;

          return (
            <article
              className="result-card"
              key={plant.id || plant.name}
              onClick={() => navigate(`/plant/${plant.id}`)}
              style={{ cursor: 'pointer' }}
            >
              <div className="result-card-top">
                <div className="result-plant-name">
                  <FaLeaf />
                  <span>{plant.name}</span>
                </div>
                {typeof plant.confidence === 'number' && (
                  <span className="confidence-badge">{(plant.confidence * 100).toFixed(0)}%</span>
                )}
              </div>

              {plant.scientific_name && <p className="result-science">{plant.scientific_name}</p>}
              {plant.usage && <p className="result-usage">{plant.usage}</p>}

              <p className="result-meta">{pointCount > 0 ? `${pointCount} điểm được đánh dấu trên bản đồ` : 'Chưa có tọa độ phân bố'}</p>
            </article>
          );
        })}
      </div>
    </div>
  );
}

export default MapPage;
