import React, { useState, useRef } from 'react';
import { Link } from 'react-router-dom';
import { FaPaperPlane, FaImage, FaTimes, FaLeaf, FaRobot, FaUser, FaMapMarkerAlt } from 'react-icons/fa';
import { sendChatMessage } from '../services/api';
import DistributionMap from '../components/DistributionMap';
import './ChatbotPage.css';

function ChatbotPage() {
  const [messages, setMessages] = useState([
    {
      type: 'bot',
      text: 'Xin chào! Tôi là trợ lý AI cây thuốc nam Việt Nam. 🌿\n\nBạn có thể:\n- **Mô tả cây thuốc nam** (VD: lá có lông, có quả, hoa trắng)\n- **Tải lên ảnh** cây thuốc nam để nhận diện\n- Hoặc **cả hai** cùng lúc!',
      plants: [],
    },
  ]);
  const [inputText, setInputText] = useState('');
  const [selectedImage, setSelectedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [showMap, setShowMap] = useState(null); // plant index để hiện map
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

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

  const handleSend = async () => {
    if (!inputText.trim() && !selectedImage) return;

    // Thêm tin nhắn của user
    const userMsg = {
      type: 'user',
      text: inputText.trim() || '(Đã gửi ảnh)',
      image: imagePreview,
    };
    setMessages((prev) => [...prev, userMsg]);

    const msgText = inputText.trim();
    const msgImage = selectedImage;

    // Reset input
    setInputText('');
    removeImage();
    setLoading(true);

    try {
      const response = await sendChatMessage({
        message: msgText || null,
        image: msgImage,
        sessionId,
      });

      setSessionId(response.session_id);

      const botMsg = {
        type: 'bot',
        text: response.reply,
        plants: response.recommended_plants || [],
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        {
          type: 'bot',
          text: 'Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại.',
          plants: [],
        },
      ]);
    } finally {
      setLoading(false);
      setTimeout(scrollToBottom, 100);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey)   {
      e.preventDefault();
      handleSend();
    }
  };

  const toggleMap = (plantId) => {
    setShowMap((prev) => (prev === plantId ? null : plantId));
  };

  // Gather tất cả coords từ recommended plants cho combined map
  const getAllDistributionCoords = (plants) => {
    const allCoords = [];
    plants.forEach((p) => {
      if (p.distribution_coords) {
        p.distribution_coords.forEach((c) => {
          allCoords.push({ ...c, location: `${p.name} - ${c.location}` });
        });
      }
    });
    return allCoords;
  };

  return (
    <div className="chatbot-page">
      <div className="chat-container">
        {/* Messages */}
        <div className="messages-area">
          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.type}`}>
              <div className="message-avatar">
                {msg.type === 'bot' ? <FaRobot /> : <FaUser />}
              </div>
              <div className="message-content">
                {msg.image && (
                  <div className="message-image">
                    <img src={msg.image} alt="Uploaded" />
                  </div>
                )}
                <div className="message-text">
                  {msg.text.split('\n').map((line, i) => (
                    <p key={i}>
                      {line.split(/(\*\*.*?\*\*)/).map((part, j) => {
                        if (part.startsWith('**') && part.endsWith('**')) {
                          return <strong key={j}>{part.slice(2, -2)}</strong>;
                        }
                        return part;
                      })}
                    </p>
                  ))}
                </div>

                {/* Recommended plants */}
                {msg.plants && msg.plants.length > 0 && (
                  <div className="recommended-plants">
                    <h4>🌿 Cây thuốc nam gợi ý:</h4>
                    {msg.plants.map((plant, pIdx) => (
                      <div key={pIdx} className="recommended-plant-card">
                        <div className="rec-plant-header">
                          <Link to={`/plant/${plant.id}`} className="rec-plant-name">
                            <FaLeaf className="rec-icon" />
                            {plant.name}
                            {plant.scientific_name && (
                              <span className="rec-scientific"> ({plant.scientific_name})</span>
                            )}
                          </Link>
                          {plant.confidence && (
                            <span className="confidence-badge">
                              {(plant.confidence * 100).toFixed(0)}%
                            </span>
                          )}
                        </div>
                        {plant.usage && (
                          <p className="rec-usage">{plant.usage}</p>
                        )}
                        {plant.distribution_coords && plant.distribution_coords.length > 0 && (
                          <button
                            className="show-map-btn"
                            onClick={() => toggleMap(`${idx}-${pIdx}`)}
                          >
                            <FaMapMarkerAlt />
                            {showMap === `${idx}-${pIdx}` ? 'Ẩn bản đồ' : 'Xem bản đồ phân bố'}
                          </button>
                        )}
                        {showMap === `${idx}-${pIdx}` && plant.distribution_coords && (
                          <div className="inline-map">
                            <DistributionMap
                              coords={plant.distribution_coords}
                              plantName={plant.name}
                              height="300px"
                            />
                          </div>
                        )}
                      </div>
                    ))}

                    {/* Combined map button */}
                    {msg.plants.length > 1 && (
                      <>
                        <button
                          className="show-map-btn combined-map-btn"
                          onClick={() => toggleMap(`combined-${idx}`)}
                        >
                          <FaMapMarkerAlt />
                          {showMap === `combined-${idx}` ? 'Ẩn bản đồ tổng hợp' : 'Xem bản đồ tổng hợp tất cả'}
                        </button>
                        {showMap === `combined-${idx}` && (
                          <div className="inline-map">
                            <DistributionMap
                              coords={getAllDistributionCoords(msg.plants)}
                              plantName="Tổng hợp"
                              height="400px"
                            />
                          </div>
                        )}
                      </>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="message bot">
              <div className="message-avatar"><FaRobot /></div>
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span><span></span><span></span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Image preview */}
        {imagePreview && (
          <div className="image-preview-bar">
            <img src={imagePreview} alt="Preview" />
            <button onClick={removeImage} className="remove-image-btn">
              <FaTimes />
            </button>
          </div>
        )}

        {/* Input area */}
        <div className="input-area">
          <input
            type="file"
            accept="image/*"
            ref={fileInputRef}
            onChange={handleImageSelect}
            style={{ display: 'none' }}
          />
          <button
            className="upload-btn"
            onClick={() => fileInputRef.current?.click()}
            title="Tải lên ảnh"
          >
            <FaImage />
          </button>
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Nhập triệu chứng hoặc mô tả cây thuốc..."
            rows={1}
            disabled={loading}
          />
          <button
            className="send-btn"
            onClick={handleSend}
            disabled={loading || (!inputText.trim() && !selectedImage)}
            title="Gửi"
          >
            <FaPaperPlane />
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatbotPage;
