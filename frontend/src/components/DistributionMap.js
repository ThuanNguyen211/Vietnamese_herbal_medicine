import React, { useEffect, useMemo, useRef } from 'react';
import L from 'leaflet';
import './DistributionMap.css';

const DEFAULT_CENTER = [10.8, 106.7];
const DEFAULT_ZOOM = 7;
const OVERLAP_MARKER_RADIUS_METERS = 5000;
const EARTH_METERS_PER_DEGREE = 111320;

function normalizeBounds(boundsInput) {
  if (!boundsInput) {
    return null;
  }

  try {
    const normalized = L.latLngBounds(boundsInput);
    return normalized.isValid() ? normalized : null;
  } catch {
    return null;
  }
}

function clampBounds(bounds, limitBounds) {
  if (!limitBounds) {
    return bounds;
  }

  if (!bounds || !bounds.isValid()) {
    return limitBounds;
  }

  if (!bounds.intersects(limitBounds)) {
    return limitBounds;
  }

  const south = Math.max(bounds.getSouth(), limitBounds.getSouth());
  const west = Math.max(bounds.getWest(), limitBounds.getWest());
  const north = Math.min(bounds.getNorth(), limitBounds.getNorth());
  const east = Math.min(bounds.getEast(), limitBounds.getEast());

  return L.latLngBounds([south, west], [north, east]);
}

function buildCoordKey(lat, lng) {
  return `${lat.toFixed(6)}|${lng.toFixed(6)}`;
}

function spreadOverlapCoordinate(lat, lng, overlapIndex, overlapCount) {
  if (overlapCount <= 1) {
    return { lat, lng };
  }

  const slotCount = Math.min(Math.max(overlapCount, 2), 8);
  const ring = Math.floor(overlapIndex / slotCount) + 1;

  let angle;
  if (slotCount === 2) {
    const twoPointAngles = [Math.PI / 2, (3 * Math.PI) / 2];
    angle = twoPointAngles[overlapIndex % 2];
  } else {
    angle = (2 * Math.PI * (overlapIndex % slotCount)) / slotCount;
  }

  const radiusMeters = OVERLAP_MARKER_RADIUS_METERS * ring;
  const latOffset = (radiusMeters * Math.cos(angle)) / EARTH_METERS_PER_DEGREE;
  const lngDivisor = EARTH_METERS_PER_DEGREE * Math.max(Math.cos((lat * Math.PI) / 180), 0.0001);
  const lngOffset = (radiusMeters * Math.sin(angle)) / lngDivisor;

  return {
    lat: lat + latOffset,
    lng: lng + lngOffset,
  };
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
  const overlapText = coord.overlapCount > 1 ? `${coord.overlapCount} cây cùng vị trí` : null;

  return `
    <div class="distribution-tooltip-content">
      <strong class="distribution-tooltip-title">${title}</strong>
      ${scientificName ? `<div class="distribution-tooltip-science">${scientificName}</div>` : ''}
      <div class="distribution-tooltip-location">${location}</div>
      ${overlapText ? `<div class="distribution-tooltip-overlap">${overlapText}</div>` : ''}
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

function DistributionMap({
  coords,
  plantName,
  height = '400px',
  legendLabel = 'Vùng phân bố',
  initialCenter = DEFAULT_CENTER,
  initialZoom = DEFAULT_ZOOM,
  minZoom = 2,
  fitPadding = 0.2,
  maxBounds,
  fallbackBounds,
}) {
  const mapRef = useRef(null);
  const mapInstanceRef = useRef(null);

  const resolvedMaxBounds = useMemo(() => normalizeBounds(maxBounds), [maxBounds]);
  const resolvedFallbackBounds = useMemo(() => normalizeBounds(fallbackBounds), [fallbackBounds]);

  const resolvedCenter = useMemo(() => {
    if (Array.isArray(initialCenter) && initialCenter.length === 2) {
      const lat = Number(initialCenter[0]);
      const lng = Number(initialCenter[1]);

      if (Number.isFinite(lat) && Number.isFinite(lng)) {
        return [lat, lng];
      }
    }

    return DEFAULT_CENTER;
  }, [initialCenter?.[0], initialCenter?.[1]]);

  const resolvedZoom = Number.isFinite(Number(initialZoom)) ? Number(initialZoom) : DEFAULT_ZOOM;
  const resolvedMinZoom = Number.isFinite(Number(minZoom)) ? Number(minZoom) : 2;
  const resolvedFitPadding = Number.isFinite(Number(fitPadding)) ? Number(fitPadding) : 0.2;

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

  const markerCoords = useMemo(() => {
    const coordCountByKey = new Map();

    safeCoords.forEach((coord) => {
      const key = buildCoordKey(coord.lat, coord.lng);
      coordCountByKey.set(key, (coordCountByKey.get(key) || 0) + 1);
    });

    const coordCursorByKey = new Map();

    return safeCoords.map((coord) => {
      const key = buildCoordKey(coord.lat, coord.lng);
      const overlapCount = coordCountByKey.get(key) || 1;
      const overlapIndex = coordCursorByKey.get(key) || 0;
      coordCursorByKey.set(key, overlapIndex + 1);

      const spread = spreadOverlapCoordinate(coord.lat, coord.lng, overlapIndex, overlapCount);

      return {
        ...coord,
        markerLat: spread.lat,
        markerLng: spread.lng,
        overlapCount,
      };
    });
  }, [safeCoords]);

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

    const mapOptions = {
      center: resolvedCenter,
      zoom: resolvedZoom,
      scrollWheelZoom: true,
      zoomAnimation: false,
      fadeAnimation: false,
      minZoom: resolvedMinZoom,
    };

    if (resolvedMaxBounds) {
      mapOptions.maxBounds = resolvedMaxBounds;
      mapOptions.maxBoundsViscosity = 1.0;
    }

    const map = L.map(mapRef.current, mapOptions);

    // Thêm tile layer (OpenStreetMap)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      maxZoom: 18,
    }).addTo(map);

    // Thêm markers
    const markers = markerCoords.map((coord) => {
      const marker = L.marker([coord.markerLat, coord.markerLng], { icon: herbIcon }).addTo(map);

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

    if (markers.length > 0) {
      const group = L.featureGroup(markers);
      const clampedBounds = clampBounds(group.getBounds().pad(resolvedFitPadding), resolvedMaxBounds);
      map.fitBounds(clampedBounds);
    } else if (resolvedFallbackBounds) {
      map.fitBounds(clampBounds(resolvedFallbackBounds, resolvedMaxBounds));
    } else if (resolvedMaxBounds) {
      map.fitBounds(resolvedMaxBounds);
    } else {
      map.setView(resolvedCenter, resolvedZoom);
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
  }, [
    markerCoords,
    plantName,
    resolvedCenter,
    resolvedZoom,
    resolvedMinZoom,
    resolvedFitPadding,
    resolvedMaxBounds,
    resolvedFallbackBounds,
  ]);

  return (
    <div className="distribution-map-container">
      <div ref={mapRef} style={{ height, width: '100%', borderRadius: '12px' }} />
      <div className="map-legend">
        <span className="legend-marker">🌿</span>
        <span>{legendLabel} {plantName}</span>
        <span className="legend-count">{markerCoords.length} địa điểm</span>
      </div>
      {markerCoords.length === 0 && <p className="no-map-data">Chưa có tọa độ, bản đồ đang hiển thị vùng mặc định.</p>}
    </div>
  );
}

export default DistributionMap;
