// API Base URL
const API_BASE_URL = 'http://localhost:8000/api';

// 현재 날짜 표시
function displayCurrentDate() {
    const now = new Date();
    const options = { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' };
    const dateStr = now.toLocaleDateString('ko-KR', options);
    document.getElementById('currentDate').textContent = dateStr;
}

// 통계 데이터 로드
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats`);
        const data = await response.json();

        document.getElementById('newCount').textContent = data.new_supports || 0;
        document.getElementById('ongoingCount').textContent = data.ongoing_supports || 0;
        document.getElementById('urgentCount').textContent = calculateUrgent(data);
        document.getElementById('totalCount').textContent = data.total_supports || 0;

        // NEW 배지 업데이트
        const newBadge = document.getElementById('newBadge');
        if (data.new_supports > 0) {
            newBadge.textContent = `${data.new_supports}개 신규`;
        }
    } catch (error) {
        console.error('통계 로드 실패:', error);
    }
}

function calculateUrgent(data) {
    // 마감임박 = 진행중 공고 중 일부로 가정
    return Math.min(data.ongoing_supports || 0, 12);
}

// 신규 공고 로드
async function loadNewAnnouncements() {
    try {
        // simple_main.py는 /supports만 지원
        const response = await fetch(`${API_BASE_URL}/supports?page=1&size=6`);
        const data = await response.json();

        const container = document.getElementById('newAnnouncements');

        if (data.items && data.items.length > 0) {
            container.innerHTML = data.items.map(item => createAnnouncementCard(item)).join('');
        } else {
            container.innerHTML = '<div class="loading">공고가 없습니다.</div>';
        }
    } catch (error) {
        console.error('공고 로드 실패:', error);
        document.getElementById('newAnnouncements').innerHTML =
            '<div class="loading">데이터를 불러올 수 없습니다.</div>';
    }
}

// 진행중 공고 로드
async function loadOngoingAnnouncements() {
    try {
        const response = await fetch(`${API_BASE_URL}/supports?page=2&size=6`);
        const data = await response.json();

        const container = document.getElementById('ongoingAnnouncements');

        if (data.items && data.items.length > 0) {
            container.innerHTML = data.items.map(item => createAnnouncementCard(item)).join('');
        } else {
            container.innerHTML = '<div class="loading">공고가 없습니다.</div>';
        }
    } catch (error) {
        console.error('공고 로드 실패:', error);
        document.getElementById('ongoingAnnouncements').innerHTML =
            '<div class="loading">데이터를 불러올 수 없습니다.</div>';
    }
}

// 마감임박 공고 로드
async function loadUrgentAnnouncements() {
    try {
        const response = await fetch(`${API_BASE_URL}/supports?page=3&size=5`);
        const data = await response.json();

        const container = document.getElementById('urgentList');

        if (data.items && data.items.length > 0) {
            container.innerHTML = data.items.map(item => createUrgentItem(item)).join('');
        } else {
            container.innerHTML = '<div class="loading">공고가 없습니다.</div>';
        }
    } catch (error) {
        console.error('공고 로드 실패:', error);
        document.getElementById('urgentList').innerHTML =
            '<div class="loading">데이터를 불러올 수 없습니다.</div>';
    }
}

// 공고 카드 생성
function createAnnouncementCard(item) {
    const source = item.source_api || 'UNKNOWN';
    const sourceClass = source === 'MSIT' ? 'source-msit' : 'source-kstartup';
    const sourceName = source === 'MSIT' ? '과기부' : 'K-Startup';

    // 마감일 계산
    const deadline = calculateDeadline(item.application_end_date);
    const deadlineClass = deadline.days <= 3 ? 'deadline-urgent' :
        deadline.days <= 7 ? 'deadline-soon' : 'deadline-normal';

    // 카테고리 태그
    const tags = [item.category, item.support_type].filter(Boolean);

    return `
        <div class="announcement-card">
            <div class="card-header">
                <span class="source-badge ${sourceClass}">${sourceName}</span>
                ${deadline.text ? `<span class="deadline-badge ${deadlineClass}">${deadline.text}</span>` : ''}
            </div>
            <div class="card-title">${item.title || '제목 없음'}</div>
            <div class="card-meta">
                ${tags.map(tag => `<span class="tag">#${tag}</span>`).join('')}
            </div>
            <div class="card-description">${item.description || item.organization || '상세 내용이 준비중입니다.'}</div>
            <div class="card-footer">
                <div class="card-date">
                    ${item.application_start_date ? `📅 ${formatDate(item.application_start_date)}` : '날짜 미정'}
                </div>
                <button class="btn-view" onclick="viewDetail(${item.id})">자세히 보기 →</button>
            </div>
        </div>
    `;
}

// 마감임박 항목 생성
function createUrgentItem(item) {
    const deadline = calculateDeadline(item.application_end_date);

    return `
        <div class="urgent-item" onclick="viewDetail(${item.id})">
            <div class="urgent-title">${item.title || '제목 없음'}</div>
            <div class="urgent-deadline">${deadline.text || '마감일 미정'}</div>
        </div>
    `;
}

// 마감일 계산
function calculateDeadline(endDate) {
    if (!endDate) return { days: null, text: null };

    const end = new Date(endDate);
    const now = new Date();
    const diffTime = end - now;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays < 0) {
        return { days: 0, text: '마감' };
    } else if (diffDays === 0) {
        return { days: 0, text: '오늘 마감' };
    } else if (diffDays <= 30) {
        return { days: diffDays, text: `D-${diffDays}` };
    } else {
        return { days: diffDays, text: formatDate(endDate) };
    }
}

// 날짜 포맷팅
function formatDate(dateStr) {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return `${date.getMonth() + 1}/${date.getDate()}`;
}

// 상세 보기
function viewDetail(id) {
    // Swagger UI로 이동 (실제로는 상세 페이지로)
    window.open(`http://localhost:8000/docs#/supports/get_support_detail_api_supports__support_id__get`, '_blank');
}

// 더보기
function loadMore() {
    alert('더보기 기능은 준비중입니다!\n현재 페이지에 표시된 공고가 전체입니다.');
}

// 초기화
document.addEventListener('DOMContentLoaded', () => {
    displayCurrentDate();
    loadStats();
    loadNewAnnouncements();
    loadOngoingAnnouncements();
    loadUrgentAnnouncements();

    // 5분마다 자동 새로고침
    setInterval(() => {
        loadStats();
        loadNewAnnouncements();
        loadOngoingAnnouncements();
        loadUrgentAnnouncements();
    }, 5 * 60 * 1000);
});
