import { useEffect, useState } from "react";
import "./NewsListPage.css";

export default function NewsListPage() {
  const [news, setNews] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [isEditMode, setIsEditMode] = useState(false);
  const [currentEditId, setCurrentEditId] = useState(null);
  const [formData, setFormData] = useState({
    title: "",
    content: "",
    published_at: "",
    is_active: true,
    image: null,
  });

  useEffect(() => {
    fetchNews();
  }, []);

  const fetchNews = () => {
    fetch("http://localhost:8000/api/news/")
      .then((response) => response.json())
      .then((data) => {
        const newsData = data.results || [];
        const sorted = newsData.sort((a, b) => new Date(b.published_at) - new Date(a.published_at));
        setNews(sorted);
      });
  };

  const handleChange = (e) => {
    const { name, value, type, checked, files } = e.target;
    if (type === "checkbox") {
      setFormData({ ...formData, [name]: checked });
    } else if (type === "file") {
      setFormData({ ...formData, [name]: files[0] });
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const data = new FormData();
    data.append("title", formData.title);
    data.append("content", formData.content);
    data.append("published_at", formData.published_at);
    data.append("is_active", formData.is_active);
    if (formData.image) {
      data.append("image", formData.image);
    }

    const url = isEditMode 
      ? `http://localhost:8000/api/news/${currentEditId}/` 
      : "http://localhost:8000/api/news/";
    const method = isEditMode ? "PUT" : "POST";

    fetch(url, {
      method: method,
      body: data,
    }).then((response) => {
      if (response.ok) {
        alert(isEditMode ? "Новость обновлена!" : "Новость создана!");
        setShowForm(false);
        setIsEditMode(false);
        setCurrentEditId(null);
        fetchNews();
        resetForm();
      } else {
        alert("Ошибка.");
      }
    });
  };

  const resetForm = () => {
    setFormData({
      title: "",
      content: "",
      published_at: "",
      is_active: true,
      image: null,
    });
  };

  const handleEdit = (item) => {
    setFormData({
      title: item.title,
      content: item.content,
      published_at: item.published_at ? item.published_at.slice(0, 16) : "",
      is_active: item.is_active,
      image: null, // не трогаем изображение
    });
    setCurrentEditId(item.id);
    setIsEditMode(true);
    setShowForm(true);
  };

  const deleteNews = (id) => {
    if (window.confirm("Удалить новость?")) {
      fetch(`http://localhost:8000/api/news/${id}/`, { method: "DELETE" }).then(() => {
        setNews((prev) => prev.filter((n) => n.id !== id));
      });
    }
  };

  return (
    <div className="news-list-wrapper">
      <h1>Все новости</h1>

      {!showForm && (
        <button className="create-button" onClick={() => { setShowForm(true); resetForm(); }}>
          Создать новость
        </button>
      )}

      {showForm && (
        <form onSubmit={handleSubmit} className="news-form">
          <label>Заголовок:</label>
          <input type="text" name="title" value={formData.title} onChange={handleChange} required />

          <label>Контент:</label>
          <textarea name="content" value={formData.content} onChange={handleChange} required />

          <label>Дата публикации:</label>
          <input type="datetime-local" name="published_at" value={formData.published_at} onChange={handleChange} />

          <label>Изображение:</label>
          <input type="file" name="image" onChange={handleChange} />

          <label>
            <input type="checkbox" name="is_active" checked={formData.is_active} onChange={handleChange} />
            Активна
          </label>

          <button type="submit">{isEditMode ? "Сохранить изменения" : "Создать"}</button>
          <button type="button" onClick={() => { setShowForm(false); setIsEditMode(false); }}>Отмена</button>
        </form>
      )}

      <ul className="news-list">
        {news.map((item) => (
          <li key={item.id} className="news-item">
            <div>{item.title}</div>
            <div>
              <button className="edit-link" onClick={() => handleEdit(item)}>Редактировать</button>
              <button className="delete-button" onClick={() => deleteNews(item.id)}>Удалить</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
