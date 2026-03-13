import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import './DistributionMap.css';

// Fix cho Leaflet marker icon
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

function DistributionMap({ coords, plantName, height = '400px' }) {
  const mapRef = useRef(null);
  const mapInstanceRef = useRef(null);

  useEffect(() => {
    if (!coords || coords.length === 0 || !mapRef.current) return;

    // Cleanup bản đồ cũ - dừng animation trước khi remove
    if (mapInstanceRef.current) {
      mapInstanceRef.current.off();
      mapInstanceRef.current.stop();
      mapInstanceRef.current.remove();
      mapInstanceRef.current = null;
    }

    // Custom green icon cho cây thuốc
    const herbIcon = L.divIcon({
      html: `<div style="
        background: #16a34a;
        width: 28px;
        height: 28px;
        border-radius: 50% 50% 50% 0;
        transform: rotate(-45deg);
        border: 2px solid white;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        justify-content: center;
      ">
        <span style="transform: rotate(45deg); color: white; font-size: 14px;">🌿</span>
      </div>`,
      className: 'herb-marker',
      iconSize: [28, 28],
      iconAnchor: [14, 28],
      popupAnchor: [0, -28],
    });

    // Tạo bản đồ với trung tâm Việt Nam
    const map = L.map(mapRef.current, {
      center: [16.0, 107.0],
      zoom: 6,
      scrollWheelZoom: true,
      zoomAnimation: false,
      fadeAnimation: false,
    });

    // Thêm tile layer (OpenStreetMap)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      maxZoom: 18,
    }).addTo(map);

    // Thêm markers
    const markers = coords.map((coord) => {
      const marker = L.marker([coord.lat, coord.lng], { icon: herbIcon }).addTo(map);
      marker.bindPopup(`
        <div style="text-align:center; min-width:150px;">
          <strong style="color:#16a34a; font-size:14px;">🌿 ${plantName}</strong>
          <br/>
          <span style="color:#475569; font-size:13px;">${coord.location}</span>
          <br/>
          <small style="color:#94a3b8;">Lat: ${coord.lat.toFixed(4)}, Lng: ${coord.lng.toFixed(4)}</small>
        </div>
      `);
      return marker;
    });

    // Fit bounds để hiển thị tất cả markers
    if (markers.length > 0) {
      const group = L.featureGroup(markers);
      map.fitBounds(group.getBounds().pad(0.3));
    }

    mapInstanceRef.current = map;

    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.off();
        mapInstanceRef.current.stop();
        mapInstanceRef.current.remove();
        mapInstanceRef.current = null;
      }
    };
  }, [coords, plantName]);

  if (!coords || coords.length === 0) {
    return <p className="no-map-data">Chưa có dữ liệu phân bố.</p>;
  }

  return (
    <div className="distribution-map-container">
      <div ref={mapRef} style={{ height, width: '100%', borderRadius: '12px' }} />
      <div className="map-legend">
        <span className="legend-marker">🌿</span>
        <span>Vùng phân bố {plantName}</span>
        <span className="legend-count">{coords.length} địa điểm</span>
      </div>
    </div>
  );
}

export default DistributionMap;
