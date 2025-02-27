
let currentPage = 1;
const pageSize = 10;

async function fetchMatches(page) {
    const response = await fetch(`http://127.0.0.1:5002/matches-list?page=${page}&pagesize=${pageSize}`);
    const data = await response.json();
    displayMatches(data.matches);
    document.getElementById('prev').disabled = page === 1;
    document.getElementById('next').disabled = data.matches.length < pageSize;
}

function displayMatches(matches) {
    const container = document.getElementById('matches');
    container.innerHTML = '';
    matches.forEach(match => {
        const matchTime = new Date(match.t).toLocaleString();
        const status = match.status==2 ? 
            `<span class="text-green-600 font-bold">${match.t1f} ${match.s1?match.s1:""} - ${match.result} - ${match.t2f} ${match.s2?match.s2:""}</span>` 
            : match.status==0 ?`<span class="text-yellow-500 font-bold">UPCOMING</span>` : `<span class="text-red-600 font-bold">LIVE</span>`;
        
        const matchDiv = document.createElement('div');
        matchDiv.classList.add("bg-white", "p-4", "rounded-lg", "shadow-lg", "border-l-4", "border-blue-500");
        matchDiv.innerHTML = `
            <h1 class="text-xl font-semibold underline">${match.sf}</h1>
            <h2 class="text-lg font-semibold">${match.t1f} <span class="text-gray-500">vs</span> ${match.t2f}</h2>
            <p class="mt-1">${status}</p>
            <p class="text-gray-500 text-sm mt-2">${matchTime}</p>
        `;
        matchDiv.addEventListener("click", () => {
            window.location.href = `matches.html?matchId=${match.mf}`;
        });
        container.appendChild(matchDiv);
    });
}

document.getElementById('prev').addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage--;
        fetchMatches(currentPage);
    }
});

document.getElementById('next').addEventListener('click', () => {
    currentPage++;
    fetchMatches(currentPage);
});

fetchMatches(currentPage);