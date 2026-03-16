import React, { useEffect, useMemo, useRef } from 'react';
import L from 'leaflet';
import './DistributionMap.css';

const SOUTH_VIETNAM_BOUNDS = L.latLngBounds(
  [7.0, 102.0],
  [13.8, 110.5]
);

function clampBoundsToSouthVietnam(bounds) {
  if (!bounds || !bounds.isValid()) {
    return SOUTH_VIETNAM_BOUNDS;
  }

  if (!bounds.intersects(SOUTH_VIETNAM_BOUNDS)) {
    return SOUTH_VIETNAM_BOUNDS;
  }

  const south = Math.max(bounds.getSouth(), SOUTH_VIETNAM_BOUNDS.getSouth());
  const west = Math.max(bounds.getWest(), SOUTH_VIETNAM_BOUNDS.getWest());
  const north = Math.min(bounds.getNorth(), SOUTH_VIETNAM_BOUNDS.getNorth());
  const east = Math.min(bounds.getEast(), SOUTH_VIETNAM_BOUNDS.getEast());

  return L.latLngBounds([south, west], [north, east]);
}

function escapeHtml(input) {
  return String(input || '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function buildTooltipContent(coord, fallbackPlantName) {
  const title = escapeHtml(coord.plantName || fallbackPlantName || 'Cây thuốc nam');
  const location = escapeHtml(coord.location || 'Vị trí không xác định');
  const scientificName = escapeHtml(coord.scientificName || '');
  const usage = escapeHtml(coord.usage || '');
  const confidenceText =
    typeof coord.confidence === 'number' ? `${Math.round(coord.confidence * 100)}%` : null;

  return `
    <div class="distribution-tooltip-content">
      <strong class="distribution-tooltip-title">${title}</strong>
      ${scientificName ? `<div class="distribution-tooltip-science">${scientificName}</div>` : ''}
      <div class="distribution-tooltip-location">${location}</div>
      ${confidenceText ? `<div class="distribution-tooltip-confidence">Độ tin cậy: ${confidenceText}</div>` : ''}
      ${usage ? `<div class="distribution-tooltip-usage">${usage.slice(0, 110)}${usage.length > 110 ? '...' : ''}</div>` : ''}
    </div>
  `;
}

// Fix cho Leaflet marker icon
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

function DistributionMap({ coords, plantName, height = '400px', legendLabel = 'Vùng phân bố' }) {
  const mapRef = useRef(null);
  const mapInstanceRef = useRef(null);

  const safeCoords = useMemo(() => {
    if (!Array.isArray(coords)) {
      return [];
    }

    return coords.filter((coord) => Number.isFinite(Number(coord?.lat)) && Number.isFinite(Number(coord?.lng))).map((coord) => ({
      ...coord,
      lat: Number(coord.lat),
      lng: Number(coord.lng),
    }));
  }, [coords]);

  useEffect(() => {
    if (!mapRef.current) return;

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

    // Tạo bản đồ và giới hạn viewport vào miền Nam Việt Nam
    const map = L.map(mapRef.current, {
      center: [10.8, 106.7],
      zoom: 7,
      scrollWheelZoom: true,
      zoomAnimation: false,
      fadeAnimation: false,
      maxBounds: SOUTH_VIETNAM_BOUNDS,
      maxBoundsViscosity: 1.0,
      minZoom: 6,
    });

    // Thêm tile layer (OpenStreetMap)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      maxZoom: 18,
    }).addTo(map);

    // Thêm markers
    const markers = safeCoords.map((coord) => {
      const marker = L.marker([coord.lat, coord.lng], { icon: herbIcon }).addTo(map);

      marker.bindTooltip(buildTooltipContent(coord, plantName), {
        direction: 'top',
        offset: [0, -24],
        opacity: 0.97,
        sticky: true,
        className: 'distribution-tooltip',
      });

      marker.on('mouseover', () => marker.openTooltip());
      marker.on('mouseout', () => marker.closeTooltip());

      return marker;
    });

    // Fit bounds nhưng luôn giữ trong khung miền Nam Việt Nam
    if (markers.length > 0) {
      const group = L.featureGroup(markers);
      const clampedBounds = clampBoundsToSouthVietnam(group.getBounds().pad(0.2));
      map.fitBounds(clampedBounds);
    } else {
      map.fitBounds(SOUTH_VIETNAM_BOUNDS);
    }

    setTimeout(() => {
      map.invalidateSize();
    }, 40);

    mapInstanceRef.current = map;

    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.off();
        mapInstanceRef.current.stop();
        mapInstanceRef.current.remove();
        mapInstanceRef.current = null;
      }
    };
  }, [safeCoords, plantName]);

  return (
    <div className="distribution-map-container">
      <div ref={mapRef} style={{ height, width: '100%', borderRadius: '12px' }} />
      <div className="map-legend">
        <span className="legend-marker">🌿</span>
        <span>{legendLabel} {plantName}</span>
        <span className="legend-count">{safeCoords.length} địa điểm</span>
      </div>
      {safeCoords.length === 0 && <p className="no-map-data">Chưa có tọa độ, bản đồ đang focus Miền Nam Việt Nam.</p>}
    </div>
  );
}

export default DistributionMap;
