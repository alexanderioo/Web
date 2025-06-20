import { useState, useEffect } from "react";
import "./FilterDemo.css";

export default function FilterDemo() {
  const [news, setNews] = useState([]);
  const [trainers, setTrainers] = useState([]);
  const [horses, setHorses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('news');
  
  // Filter states
  const [newsFilters, setNewsFilters] = useState({
    title: '',
    is_active: '',
    published_after: '',
    published_before: ''
  });
  
  const [trainerFilters, setTrainerFilters] = useState({
    name: '',
    experience_min: '',
    experience_max: ''
  });
  
  const [horseFilters, setHorseFilters] = useState({
    name: '',
    gender: '',
    description: ''
  });

  const fetchData = async (endpoint, filters) => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      Object.entries(filters).forEach(([key, value]) => {
        if (value) params.append(key, value);
      });
      
      const response = await fetch(`http://localhost:8000/api/${endpoint}/?${params}`);
      const data = await response.json();
      
      if (endpoint === 'news') setNews(data.results || data);
      else if (endpoint === 'trainers') setTrainers(data.results || data);
      else if (endpoint === 'horses') setHorses(data.results || data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData('news', newsFilters);
  }, [newsFilters]);

  useEffect(() => {
    fetchData('trainers', trainerFilters);
  }, [trainerFilters]);

  useEffect(() => {
    fetchData('horses', horseFilters);
  }, [horseFilters]);

  const handleNewsFilterChange = (field, value) => {
    setNewsFilters(prev => ({ ...prev, [field]: value }));
  };

  const handleTrainerFilterChange = (field, value) => {
    setTrainerFilters(prev => ({ ...prev, [field]: value }));
  };

  const handleHorseFilterChange = (field, value) => {
    setHorseFilters(prev => ({ ...prev, [field]: value }));
  };

  const clearFilters = (type) => {
    if (type === 'news') setNewsFilters({ title: '', is_active: '', published_after: '', published_before: '' });
    else if (type === 'trainers') setTrainerFilters({ name: '', experience_min: '', experience_max: '' });
    else if (type === 'horses') setHorseFilters({ name: '', gender: '', description: '' });
  };

  return (
    <div className="filter-demo">
      <h1>Демонстрация фильтрации Django Filter</h1>
      
      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'news' ? 'active' : ''}`}
          onClick={() => setActiveTab('news')}
        >
          Новости
        </button>
        <button 
          className={`tab ${activeTab === 'trainers' ? 'active' : ''}`}
          onClick={() => setActiveTab('trainers')}
        >
          Тренеры
        </button>
        <button 
          className={`tab ${activeTab === 'horses' ? 'active' : ''}`}
          onClick={() => setActiveTab('horses')}
        >
          Лошади
        </button>
      </div>

      {activeTab === 'news' && (
        <div className="filter-section">
          <h2>Фильтрация новостей</h2>
          <div className="filters">
            <input
              type="text"
              placeholder="Заголовок содержит..."
              value={newsFilters.title}
              onChange={(e) => handleNewsFilterChange('title', e.target.value)}
            />
            <select
              value={newsFilters.is_active}
              onChange={(e) => handleNewsFilterChange('is_active', e.target.value)}
            >
              <option value="">Все статусы</option>
              <option value="true">Активные</option>
              <option value="false">Неактивные</option>
            </select>
            <input
              type="date"
              placeholder="Опубликовано после..."
              value={newsFilters.published_after}
              onChange={(e) => handleNewsFilterChange('published_after', e.target.value)}
            />
            <input
              type="date"
              placeholder="Опубликовано до..."
              value={newsFilters.published_before}
              onChange={(e) => handleNewsFilterChange('published_before', e.target.value)}
            />
            <button onClick={() => clearFilters('news')}>Очистить фильтры</button>
          </div>
          
          {loading ? (
            <div>Загрузка...</div>
          ) : (
            <div className="results">
              <h3>Результаты ({news.length})</h3>
              {news.map(item => (
                <div key={item.id} className="result-item">
                  <h4>{item.title}</h4>
                  <p>Статус: {item.is_active ? 'Активна' : 'Неактивна'}</p>
                  <p>Дата: {item.published_at ? new Date(item.published_at).toLocaleDateString() : 'Не указана'}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {activeTab === 'trainers' && (
        <div className="filter-section">
          <h2>Фильтрация тренеров</h2>
          <div className="filters">
            <input
              type="text"
              placeholder="Имя содержит..."
              value={trainerFilters.name}
              onChange={(e) => handleTrainerFilterChange('name', e.target.value)}
            />
            <input
              type="number"
              placeholder="Опыт от (лет)..."
              value={trainerFilters.experience_min}
              onChange={(e) => handleTrainerFilterChange('experience_min', e.target.value)}
            />
            <input
              type="number"
              placeholder="Опыт до (лет)..."
              value={trainerFilters.experience_max}
              onChange={(e) => handleTrainerFilterChange('experience_max', e.target.value)}
            />
            <button onClick={() => clearFilters('trainers')}>Очистить фильтры</button>
          </div>
          
          {loading ? (
            <div>Загрузка...</div>
          ) : (
            <div className="results">
              <h3>Результаты ({trainers.length})</h3>
              {trainers.map(item => (
                <div key={item.id} className="result-item">
                  <h4>{item.profile.user.first_name} {item.profile.user.last_name}</h4>
                  <p>Опыт: {item.experience_years} лет</p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {activeTab === 'horses' && (
        <div className="filter-section">
          <h2>Фильтрация лошадей</h2>
          <div className="filters">
            <input
              type="text"
              placeholder="Имя содержит..."
              value={horseFilters.name}
              onChange={(e) => handleHorseFilterChange('name', e.target.value)}
            />
            <select
              value={horseFilters.gender}
              onChange={(e) => handleHorseFilterChange('gender', e.target.value)}
            >
              <option value="">Все</option>
              <option value="male">Жеребец</option>
              <option value="female">Кобыла</option>
            </select>
            <input
              type="text"
              placeholder="Описание содержит..."
              value={horseFilters.description}
              onChange={(e) => handleHorseFilterChange('description', e.target.value)}
            />
            <button onClick={() => clearFilters('horses')}>Очистить фильтры</button>
          </div>
          
          {loading ? (
            <div>Загрузка...</div>
          ) : (
            <div className="results">
              <h3>Результаты ({horses.length})</h3>
              {horses.map(item => (
                <div key={item.id} className="result-item">
                  <h4>{item.name}</h4>
                  <p>Пол: {item.gender === 'male' ? 'Жеребец' : 'Кобыла'}</p>
                  {item.description && <p>Описание: {item.description.substring(0, 100)}...</p>}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
} 