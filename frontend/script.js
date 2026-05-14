// script.js - логика работы сайта

// АДРЕС СЕРВЕРА
// Если сайт открыт локально (через python -m http.server), используем localhost
// Если в Docker, используем имя контейнера backend
const API_BASE = window.location.origin.includes("localhost") || window.location.origin.includes("127.0.0.1")
    ? "http://127.0.0.1:8010"
    : "http://backend:8010";

// ==========================================
// ========== ПЕРЕКЛЮЧЕНИЕ ТЕМЫ =============
// ==========================================

const themeToggle = document.getElementById('themeToggle');
themeToggle.addEventListener('click', () => {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', newTheme);
    themeToggle.textContent = newTheme === 'dark' ? '🌙' : '☀️';
});

// ==========================================
// ========== НАВИГАЦИЯ =====================
// ==========================================

document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();

        const section = link.getAttribute('data-section');

        // Прячем все секции
        document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
        // Убираем активный класс у всех ссылок
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));

        // Показываем нужную секцию
        document.getElementById(`${section}-section`).classList.add('active');
        // Делаем ссылку активной
        link.classList.add('active');

        // Загружаем данные для показанной секции
        if (section === 'students') loadStudents();
        if (section === 'disciplines') loadDisciplines();
        if (section === 'stats') loadStatsData();
    });
});

// ==========================================
// ========== ГЛАВНАЯ СТРАНИЦА ==============
// ==========================================

async function loadDashboard() {
    try {
        // Загружаем данные с сервера
        const [studentsRes, disciplinesRes, honorsRes] = await Promise.all([
            fetch(`${API_BASE}/api/students`),
            fetch(`${API_BASE}/api/disciplines`),
            fetch(`${API_BASE}/api/honors-students`)
        ]);

        const students = await studentsRes.json();
        const disciplines = await disciplinesRes.json();
        const honors = await honorsRes.json();

        // Обновляем цифры на главной
        document.getElementById('studentsCount').textContent = students.length;
        document.getElementById('disciplinesCount').textContent = disciplines.length;
        document.getElementById('honorsCount').textContent = honors.length;

        // Загружаем топ-5 студентов
        const topRes = await fetch(`${API_BASE}/api/top-students`);
        const topStudents = await topRes.json();
        const topList = document.getElementById('topStudentsList');
        topList.innerHTML = topStudents.map(s =>
            `<div class="list-item"><strong>${s.name}</strong> (${s.group}) — ${s.average_score.toFixed(2)}</div>`
        ).join('');

        // Загружаем отличников
        const honorsList = document.getElementById('honorsList');
        honorsList.innerHTML = honors.map(s =>
            `<div class="list-item"><strong>${s.name}</strong> (${s.group}) — ${s.average_score.toFixed(2)}</div>`
        ).join('');

    } catch(e) {
        console.error('Ошибка загрузки:', e);
    }
}

// ==========================================
// ========== СТУДЕНТЫ ======================
// ==========================================

async function loadStudents() {
    try {
        const res = await fetch(`${API_BASE}/api/students`);
        const students = await res.json();

        const container = document.getElementById('studentsList');
        container.innerHTML = students.map(s => `
            <div class="student-card">
                <h4>${s.name}</h4>
                <p>Группа: ${s.group}</p>
                <p>Средний балл: ${s.average_score ? s.average_score.toFixed(2) : 'Нет оценок'}</p>
                <button class="btn btn-danger" onclick="deleteStudent(${s.id})">Удалить</button>
                <button class="btn btn-secondary" onclick="openGradeModal(${s.id}, '${s.name}')">➕ Оценка</button>
            </div>
        `).join('');
    } catch(e) {
        console.error(e);
    }
}

// Функция удаления студента (доступна глобально)
window.deleteStudent = async (id) => {
    if (confirm('Удалить студента? Все его оценки тоже удалятся.')) {
        await fetch(`${API_BASE}/api/students/${id}`, { method: 'DELETE' });
        loadStudents();      // Обновляем список
        loadDashboard();     // Обновляем главную
    }
};

// Кнопка добавления студента
document.getElementById('addStudentBtn')?.addEventListener('click', async () => {
    const name = document.getElementById('studentName').value;
    const group = document.getElementById('studentGroup').value;

    if (!name || !group) {
        alert('Заполните все поля!');
        return;
    }

    await fetch(`${API_BASE}/api/students`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, group })
    });

    // Очищаем поля
    document.getElementById('studentName').value = '';
    document.getElementById('studentGroup').value = '';

    // Обновляем данные
    loadStudents();
    loadDashboard();
});

// ==========================================
// ========== ДИСЦИПЛИНЫ ====================
// ==========================================

async function loadDisciplines() {
    try {
        const res = await fetch(`${API_BASE}/api/disciplines`);
        const disciplines = await res.json();

        const container = document.getElementById('disciplinesList');
        container.innerHTML = disciplines.map(d => `
            <div class="discipline-card">
                <h4>${d.name}</h4>
                <p>Кредиты: ${d.credits}</p>
            </div>
        `).join('');

        // Обновляем выпадающие списки (для оценок и статистики)
        const select = document.getElementById('disciplineSelect');
        if (select) {
            select.innerHTML = '<option value="">Выберите дисциплину</option>' +
                disciplines.map(d => `<option value="${d.id}">${d.name}</option>`).join('');
        }

        const gradeSelect = document.getElementById('gradeDisciplineSelect');
        if (gradeSelect) {
            gradeSelect.innerHTML = '<option value="">Выберите дисциплину</option>' +
                disciplines.map(d => `<option value="${d.id}">${d.name}</option>`).join('');
        }
    } catch(e) {
        console.error(e);
    }
}

// Кнопка добавления дисциплины
document.getElementById('addDisciplineBtn')?.addEventListener('click', async () => {
    const name = document.getElementById('disciplineName').value;
    const credits = document.getElementById('disciplineCredits').value;

    if (!name || !credits) {
        alert('Заполните все поля!');
        return;
    }

    await fetch(`${API_BASE}/api/disciplines`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, credits: parseInt(credits) })
    });

    document.getElementById('disciplineName').value = '';
    document.getElementById('disciplineCredits').value = '';

    loadDisciplines();
    loadDashboard();
});

// ==========================================
// ========== СТАТИСТИКА ====================
// ==========================================

document.getElementById('showRatingBtn')?.addEventListener('click', async () => {
    const disciplineId = document.getElementById('disciplineSelect').value;
    if (!disciplineId) {
        alert('Выберите дисциплину!');
        return;
    }

    const res = await fetch(`${API_BASE}/api/discipline-rating/${disciplineId}`);
    const data = await res.json();

    const container = document.getElementById('disciplineRating');
    container.innerHTML = `<h3>${data.discipline}</h3>` +
        data.students.map(s => `<div class="list-item">${s.name} — ${s.score}</div>`).join('');
});

// ==========================================
// ========== ОЦЕНКИ (МОДАЛЬНОЕ ОКНО) ========
// ==========================================

let currentStudentId = null;

window.openGradeModal = async (studentId, studentName) => {
    currentStudentId = studentId;
    await loadDisciplines();  // Загружаем список дисциплин для выпадающего списка

    const modal = document.getElementById('gradeModal');
    modal.classList.add('active');

    // Заполняем выпадающий список студентов (только текущий)
    document.getElementById('gradeStudentSelect').innerHTML = `<option value="${studentId}">${studentName}</option>`;
};

// Закрыть модальное окно
document.querySelector('#gradeModal .close')?.addEventListener('click', () => {
    document.getElementById('gradeModal').classList.remove('active');
});

// Сохранить оценку
document.getElementById('saveGradeBtn')?.addEventListener('click', async () => {
    const disciplineId = document.getElementById('gradeDisciplineSelect').value;
    const score = parseFloat(document.getElementById('gradeScore').value);

    if (!currentStudentId || !disciplineId || !score) {
        alert('Заполните все поля!');
        return;
    }

    await fetch(`${API_BASE}/api/grades`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            student_id: currentStudentId,
            discipline_id: parseInt(disciplineId),
            score: score
        })
    });

    document.getElementById('gradeModal').classList.remove('active');
    document.getElementById('gradeScore').value = '';

    loadStudents();      // Обновляем список студентов
    loadDashboard();     // Обновляем главную
});

async function loadStatsData() {
    await loadDisciplines();
}

// ==========================================
// ========== ЗАПУСК ========================
// ==========================================

// Загружаем все данные при открытии страницы
loadDashboard();
loadStudents();
loadDisciplines();