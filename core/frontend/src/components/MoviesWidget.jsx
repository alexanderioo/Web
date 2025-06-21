import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./MoviesWidget.css";

export default function MoviesWidget() {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [favorites, setFavorites] = useState(new Set());

  useEffect(() => {
    // Имитация загрузки данных о фильмах
    // В реальном проекте здесь был бы API запрос
    const mockMovies = [
      {
        id: 1,
        title_ru: "Аватар 3",
        title_en: "Avatar 3",
        image: "https://via.placeholder.com/150x200/4CAF50/FFFFFF?text=Avatar+3",
        release_date: "2024-12-20",
        description: "Продолжение эпической саги Джеймса Кэмерона"
      },
      {
        id: 2,
        title_ru: "Дюна: Часть вторая",
        title_en: "Dune: Part Two",
        image: "https://via.placeholder.com/150x200/2196F3/FFFFFF?text=Dune+2",
        release_date: "2024-03-15",
        description: "Завершение истории Пола Атрейдеса"
      },
      {
        id: 3,
        title_ru: "Мертвецы не умирают",
        title_en: "The Dead Don't Die",
        image: "https://via.placeholder.com/150x200/FF9800/FFFFFF?text=Dead+Don't+Die",
        release_date: "2024-06-10",
        description: "Зомби-комедия от Джима Джармуша"
      },
      {
        id: 4,
        title_ru: "Интерстеллар 2",
        title_en: "Interstellar 2",
        image: "https://via.placeholder.com/150x200/9C27B0/FFFFFF?text=Interstellar+2",
        release_date: "2024-09-05",
        description: "Новое космическое путешествие"
      },
      {
        id: 5,
        title_ru: "Матрица: Воскрешение",
        title_en: "The Matrix: Resurrection",
        image: "https://via.placeholder.com/150x200/F44336/FFFFFF?text=Matrix+4",
        release_date: "2024-11-15",
        description: "Возвращение в цифровой мир"
      }
    ];

    setMovies(mockMovies);
    setLoading(false);
  }, []);

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

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    });
  };

  return (
    <div className="movies-widget">
      <div className="widget-title-container">
        <h2 className="widget-title">Премьеры месяца</h2>
      </div>
      
      {loading ? (
        <div className="loading">Загрузка премьер...</div>
      ) : (
        <>
          <ol className="movies-list">
            {movies.map((movie, index) => (
              <li key={movie.id} className="movie-item">
                <div className="movie-number">{index + 1}</div>
                <div className="movie-content">
                  <img 
                    src={movie.image} 
                    alt={movie.title_ru} 
                    className="movie-poster"
                  />
                  <div className="movie-info">
                    <h3 className="movie-title-ru" onClick={() => window.open(`/movie/${movie.id}`, '_blank')}>
                      {movie.title_ru}
                    </h3>
                    <h4 className="movie-title-en">{movie.title_en}</h4>
                    <p className="movie-date">{formatDate(movie.release_date)}</p>
                    <p className="movie-description">{movie.description}</p>
                  </div>
                  <button 
                    className={`favorite-button ${favorites.has(movie.id) ? 'active' : ''}`}
                    onClick={() => toggleFavorite(movie.id)}
                    title={favorites.has(movie.id) ? 'Удалить из избранного' : 'Добавить в избранное'}
                  >
                    {favorites.has(movie.id) ? '★' : '☆'}
                  </button>
                </div>
              </li>
            ))}
          </ol>
          
          <div className="calendar-link-container">
            <Link to="/calendar" className="calendar-link">
              📅 Календарь премьер
            </Link>
          </div>
        </>
      )}
    </div>
  );
} 