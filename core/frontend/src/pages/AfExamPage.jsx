import { useEffect, useState } from "react";

export default function AfExamPage() {
  const FIO = "Фролов Александр Дмитриевич";
  const GROUP = "231-322";

  const [exams, setExams] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/afexam/")
      .then((res) => res.json())
      .then((data) => {
        setExams(data.results || data);
        setLoading(false);
      });
  }, []);

  return (
    <div className="afexam-page container">
      <h1>Экзамены</h1>
      <h2>{FIO} — группа {GROUP}</h2>
      {loading ? (
        <p>Загрузка...</p>
      ) : (
        <div>
          {exams.length === 0 ? (
            <p>Нет опубликованных экзаменов.</p>
          ) : (
            <table className="afexam-table">
              <thead>
                <tr>
                  <th>Название экзамена</th>
                  <th>Дата создания</th>
                  <th>Дата проведения</th>
                  <th>Задание (картинка)</th>
                  <th>Пользователи (email)</th>
                </tr>
              </thead>
              <tbody>
                {exams.filter(e => e.is_public).map((exam) => (
                  <tr key={exam.id}>
                    <td>{exam.title}</td>
                    <td>{new Date(exam.created_at).toLocaleString()}</td>
                    <td>{new Date(exam.date).toLocaleString()}</td>
                    <td>
                      {exam.image ? (
                        <img src={exam.image} alt="Задание" style={{maxWidth: 320, maxHeight: 200}} />
                      ) : (
                        <span>Нет изображения</span>
                      )}
                    </td>
                    <td>
                      {exam.users && exam.users.length > 0 ? (
                        <ul style={{margin: 0, paddingLeft: 18}}>
                          {exam.users.map((email, idx) => (
                            <li key={idx}>{email}</li>
                          ))}
                        </ul>
                      ) : (
                        <span>Нет пользователей</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
} 