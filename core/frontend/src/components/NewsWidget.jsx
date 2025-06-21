import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./NewsWidget.css";

export default function NewsWidget() {
  const [news, setNews] = useState([]);
  const [selectedNews, setSelectedNews] = useState(null);
  const [loading, setLoading] = useState(false);
  // NOTE: Favorite state is not implemented on the backend
  const [favorites, setFavorites] = useState(new Set());

  useEffect(() => {
    setLoading(true);
    fetch("http://localhost:8000/api/news/")
      .then((response) => response.json())
      .then((data) => {
        const newsData = data.results || [];
        const sorted = newsData.sort((a, b) => new Date(b.published_at) - new Date(a.published_at));
        setNews(sorted.slice(0, 5)); // Top 5 news
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching news:", error);
        setLoading(false);
      });
  }, []);

  const openDetail = (id) => {
    setLoading(true);
    fetch(`http://localhost:8000/api/news/${id}/`)
      .then((response) => response.json())
      .then((data) => {
        setSelectedNews(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching news detail:", error);
        setLoading(false);
      });
  };
  
  const closeDetail = () => {
    setSelectedNews(null);
  };

  const toggleFavorite = (id) => {
    setFavorites(prevFavorites => {
        const newFavorites = new Set(prevFavorites);
        if (newFavorites.has(id)) {
            newFavorites.delete(id);
        } else {
            newFavorites.add(id);
        }
        return newFavorites;
    });
  };

  return (
    <div className="news-widget">
      <div className="widget-title-container">
        <h2 className="widget-title">Последние новости</h2>
      </div>

      {loading && !selectedNews && <div>Загрузка...</div>}

      {!selectedNews && !loading && (
        <>
          <ol className="news-list-widget">
            {news.map((item) => (
              <li key={item.id} className="news-item-widget">
                {item.image && (
                  <img className="news-image-widget" src={item.image} alt={item.title} onClick={() => openDetail(item.id)}/>
                )}
                <div className="news-content-widget">
                  <h3 className="news-title-widget" onClick={() => openDetail(item.id)}>
                    {item.title}
                  </h3>
                  {item.title_en && (
                    <h4 className="news-title-en-widget" onClick={() => openDetail(item.id)}>
                      {item.title_en}
                    </h4>
                  )}
                  <p className="published-date">
                    {item.published_at
                      ? new Date(item.published_at).toLocaleDateString()
                      : "Без даты"}
                  </p>
                </div>
                <button 
                  className={`favorite-button ${favorites.has(item.id) ? 'active' : ''}`}
                  onClick={() => toggleFavorite(item.id)}
                >
                  &#9733; {/* Star icon */}
                </button>
              </li>
            ))}
          </ol>
          <div className="all-news-link-container">
            <Link to="/news" className="button">Все новости</Link>
          </div>
        </>
      )}

      {selectedNews && !loading && (
        <div className="news-detail-wrapper">
          {selectedNews.image && <img src={selectedNews.image} alt={selectedNews.title} className="news-detail-image"/>}
          <h1>{selectedNews.title}</h1>
          <p className="published-date">
            {selectedNews.published_at
              ? new Date(selectedNews.published_at).toLocaleDateString()
              : "Без даты публикации"}
          </p>
          <div dangerouslySetInnerHTML={{ __html: selectedNews.content }} />
          <button onClick={closeDetail} className="button back-button">Назад к новостям</button>
        </div>
      )}
    </div>
  );
}
