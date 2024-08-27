document.addEventListener('DOMContentLoaded', () => {
    const startButton = document.getElementById('start-button');
    const moveForm = document.getElementById('move-form');
    const boardElement = document.querySelector('#board tbody');

    startButton.addEventListener('click', () => {
        fetch('/start_game', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.message === "Game started") {
                    createBoard(data.board_state);
                    moveForm.style.display = 'block'; // Show the move form
                }
            });
    });

    document.getElementById('move-form').addEventListener('submit', (event) => {
        event.preventDefault();
        
        const player = document.getElementById('player').value;
        const figureName = document.getElementById('figure-name').value;
        const direction = document.getElementById('direction').value;
        
        fetch('/move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ player, figure_name: figureName, direction })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === "Move successful") {
                createBoard(data.board_state);
            } else {
                alert('Move failed: ' + (data.error || 'Unknown error'));
            }
        });
    });

    function createBoard(boardState) {
        boardElement.innerHTML = '';
        boardState.forEach(row => {
            const rowElement = document.createElement('tr');
            row.forEach(cell => {
                const cellElement = document.createElement('td');
                cellElement.textContent = cell === null ? '-' : cell;
                cellElement.className = cell === '-' ? 'empty' : '';
                rowElement.appendChild(cellElement);
            });
            boardElement.appendChild(rowElement);
        });
    }
});
