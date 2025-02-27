const urlParams = new URLSearchParams(window.location.search);
        const matchId = urlParams.get("matchId");

        if (!matchId) {
            alert("Match ID is missing!");
            window.location.href = "index.html";
        }

        document.getElementById("matchTitle").textContent = `Match ${matchId}`;

        const socket = new WebSocket(`ws://127.0.0.1:5002/live-updates/${matchId}`);

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            document.getElementById("matchTitle").textContent = `${data.a.split(".")[0]} VS ${data.a.split(".")[1]}`;
            document.getElementById("playing").textContent = `${data.p.split(".")[0]}(${data.q.split(".")[0] || ""})  ${data.p.split(".")[1] || ""}(${data.q.split(".")[1] || ""})`;
            document.getElementById("score").textContent = `${data.k || "yet to bat"} (${data.j})`;
            document.getElementById("currentOver").textContent = data.d;
            document.getElementById("lastOver").textContent = data.l;
            document.getElementById("status").textContent = data.B === "B" ? "Ball" : data.B === "^2" ? "Caught Out" : data.B;
        };

        async function fetchScorecard() {
            try {
                const response = await fetch(`/scorecard/${matchId}`);
                const scorecardData = await response.json();
                renderScorecard(scorecardData);
            } catch (error) {
                console.error("Error fetching scorecard:", error);
            }
        }

        function renderScorecard(scorecardData) {
            document.getElementById("team1-batting").innerHTML = createBattingTable("Team 1 Batting", scorecardData[0].b);
            document.getElementById("team1-bowling").innerHTML = createBowlingTable("Team 1 Bowling", scorecardData[0].a);
            if (scorecardData[1].a){
            document.getElementById("team2-batting").innerHTML = createBattingTable("Team 2 Batting", scorecardData[1].b);
            document.getElementById("team2-bowling").innerHTML = createBowlingTable("Team 2 Bowling", scorecardData[1].a);
            }
        }

        function createBattingTable(title, players) {
            return `
                <h3 class="text-lg font-bold mb-2">${title}</h3>
                <table class="w-full border-collapse border border-gray-600">
                    <thead>
                        <tr class="bg-gray-700">
                            <th class="border border-gray-600 px-2 py-1">Player</th>
                            <th class="border border-gray-600 px-2 py-1">Runs</th>
                            <th class="border border-gray-600 px-2 py-1">Balls</th>
                            <th class="border border-gray-600 px-2 py-1">4s</th>
                            <th class="border border-gray-600 px-2 py-1">6s</th>
                            <th class="border border-gray-600 px-2 py-1">Wicket By</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${players.map(player => {
                            const data = player.split(".");
                            return `
                                <tr>
                                    <td class="border border-gray-600 px-2 py-1">${data[0]}</td>
                                    <td class="border border-gray-600 px-2 py-1">${data[1]||" "}</td>
                                    <td class="border border-gray-600 px-2 py-1">${data[2]||" "}</td>
                                    <td class="border border-gray-600 px-2 py-1">${data[3]||" "}</td>
                                    <td class="border border-gray-600 px-2 py-1">${data[4]||" "}</td>
                                    <td class="border border-gray-600 px-2 py-1">${data[8]?data[8].replaceAll("/"," ").replaceAll("-",""): ""} - ${data[9]?data[9].split("/")[0]: ""}</td>
                                </tr>
                            `;
                        }).join("")}
                    </tbody>
                </table>
            `;
        }

        function createBowlingTable(title, players) {
            return `
                <h3 class="text-lg font-bold mb-2">${title}</h3>
                <table class="w-full border-collapse border border-gray-600">
                    <thead>
                        <tr class="bg-gray-700">
                            <th class="border border-gray-600 px-2 py-1">Bowler</th><th class="border border-gray-600 px-2 py-1">Runs</th><th class="border border-gray-600 px-2 py-1">Overs</th><th class="border border-gray-600 px-2 py-1">Maidens</th><th class="border border-gray-600 px-2 py-1">Wickets</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${players.map(player => {
                            const data = player.split(".");
                            return `<tr>
                                <td class="border border-gray-600 px-2 py-1">${data[0]}</td><td class="border border-gray-600 px-2 py-1">${data[1]}</td><td class="border border-gray-600 px-2 py-1">${data[2]/6}</td>
                                <td class="border border-gray-600 px-2 py-1">${data[3]}</td><td class="border border-gray-600 px-2 py-1">${data[4]}</td>
                            </tr>`;
                        }).join("")}
                    </tbody>
                </table>`;
        }

        document.querySelectorAll(".tab-btn").forEach(button => {
            button.addEventListener("click", () => {
                document.querySelectorAll(".tab-content").forEach(tab => tab.classList.add("hidden"));
                document.getElementById(`${button.dataset.tab}-tab`).classList.remove("hidden");
                if (button.dataset.tab === "scorecard") fetchScorecard();
            });
        });