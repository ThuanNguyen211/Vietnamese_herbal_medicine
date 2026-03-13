import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { FaArrowLeft, FaLeaf, FaMapMarkerAlt, FaSeedling, FaMortarPestle, FaStethoscope, FaInfoCircle, FaCut } from 'react-icons/fa';
import { getPlantDetail } from '../services/api';
import DistributionMap from '../components/DistributionMap';
import './PlantDetailPage.css';

function PlantDetailPage() {
  const { id } = useParams();
  const [plant, setPlant] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadPlant();
  }, [id]);

  const loadPlant = async () => {
    try {
      setLoading(true);
      const data = await getPlantDetail(id);
      setPlant(data);
    } catch (err) {
      setError('Không tìm thấy cây thuốc nam.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <FaLeaf className="loading-icon spin" />
        <p>Đang tải thông tin...</p>
      </div>
    );
  }

  if (error || !plant) {
    return (
      <div className="error-container">
        <p>{error || 'Không tìm thấy'}</p>
        <Link to="/" className="back-btn"><FaArrowLeft /> Quay lại danh mục</Link>
      </div>
    );
  }

  return (
    <div className="plant-detail-page">
      <Link to="/" className="back-link">
        <FaArrowLeft /> Quay lại danh mục
      </Link>

      <div className="plant-detail-card">
        {/* Header */}
        <div className="detail-header">
          <div className="detail-image">
            {plant.image_url ? (
              <img src={`http://localhost:8000${plant.image_url}`} alt={plant.name} />
            ) : (
              <div className="image-placeholder">
                <FaLeaf />
              </div>
            )}
          </div>
          <div className="detail-title">
            <h1>{plant.name}</h1>
            {plant.scientific_name && (
              <p className="scientific-name">{plant.scientific_name}</p>
            )}
            {plant.family && (
              <p className="family-name">Họ: {plant.family}</p>
            )}
            {plant.other_names && (
              <p className="other-names">Tên khác: {plant.other_names}</p>
            )}
          </div>
        </div>

        {/* Info sections */}
        <div className="detail-sections">
          {plant.description && (
            <div className="detail-section">
              <h3><FaInfoCircle className="section-icon" /> Mô tả</h3>
              <p>{plant.description}</p>
            </div>
          )}

          {plant.parts_used && (
            <div className="detail-section">
              <h3><FaCut className="section-icon" /> Bộ phận dùng</h3>
              <p>{plant.parts_used}</p>
            </div>
          )}

          {plant.usage && (
            <div className="detail-section">
              <h3><FaSeedling className="section-icon" /> Công dụng</h3>
              <p>{plant.usage}</p>
            </div>
          )}

          {plant.preparation && (
            <div className="detail-section">
              <h3><FaMortarPestle className="section-icon" /> Cách dùng / Bào chế</h3>
              <p>{plant.preparation}</p>
            </div>
          )}

          {plant.symptoms && (
            <div className="detail-section">
              <h3><FaStethoscope className="section-icon" /> Triệu chứng điều trị</h3>
              <div className="symptom-tags">
                {plant.symptoms.split(',').map((s, i) => (
                  <span key={i} className="symptom-tag">{s.trim()}</span>
                ))}
              </div>
            </div>
          )}

          {/* Distribution Map */}
          {plant.distribution_coords && plant.distribution_coords.length > 0 && (
            <div className="detail-section">
              <h3><FaMapMarkerAlt className="section-icon" /> Bản đồ phân bố</h3>
              {plant.distribution && <p className="distribution-text">{plant.distribution}</p>}
              <DistributionMap
                coords={plant.distribution_coords}
                plantName={plant.name}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default PlantDetailPage;
