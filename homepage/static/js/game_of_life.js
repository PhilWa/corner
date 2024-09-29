const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let gridSize = 50; // Initial grid size (cells per row/column)
let grid;
let nextGrid;
let cellSize;
let gridWidth;
let gridHeight;
let transitionProgress = 0;
const transitionDuration = 500; // Duration of transition in milliseconds
const updateInterval = 800; // Time between updates in milliseconds

// Function to resize canvas and adjust cell size
function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    cellSize = Math.min(canvas.width / gridSize, canvas.height / gridSize);
    gridWidth = Math.ceil(canvas.width / cellSize);
    gridHeight = Math.ceil(canvas.height / cellSize);
}

// Initialize the grid and canvas
function init() {
    resizeCanvas();
    grid = createGrid();
    nextGrid = createGrid();
    drawGrid();
    setInterval(() => {
        updateGrid();
        transitionProgress = 0;
    }, updateInterval);
}

// Recalculate on window resize
window.addEventListener('resize', () => {
    resizeCanvas();
    grid = createGrid();
    nextGrid = createGrid();
    drawGrid();
});

// Rest of your Game of Life functions
function createGrid() {
    let grid = new Array(gridWidth);
    for (let i = 0; i < gridWidth; i++) {
        grid[i] = new Array(gridHeight);
        for (let j = 0; j < gridHeight; j++) {
            grid[i][j] = Math.random() > 0.8 ? 1 : 0;
        }
    }
    return grid;
}

function drawGrid() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let x = 0; x < gridWidth; x++) {
        for (let y = 0; y < gridHeight; y++) {
            let currentState = grid[x][y];
            let nextState = nextGrid[x][y];
            let cellValue = currentState + (nextState - currentState) * (transitionProgress / transitionDuration);

            ctx.fillStyle = `rgba(0, 0, 0, ${cellValue})`;
            ctx.fillRect(
                x * cellSize,
                y * cellSize,
                cellSize,
                cellSize
            );
        }
    }
}

function updateGrid() {
    for (let x = 0; x < gridWidth; x++) {
        for (let y = 0; y < gridHeight; y++) {
            let neighbors = countNeighbors(x, y);
            if (grid[x][y] === 1) {
                nextGrid[x][y] = (neighbors === 2 || neighbors === 3) ? 1 : 0;
            } else {
                nextGrid[x][y] = (neighbors === 3) ? 1 : 0;
            }
        }
    }
    // Swap grids
    [grid, nextGrid] = [nextGrid, grid];
}

function createEmptyGrid() {
    let grid = new Array(gridSize);
    for (let i = 0; i < gridSize; i++) {
        grid[i] = new Array(gridSize).fill(0);
    }
    return grid;
}

function countNeighbors(x, y) {
    let count = 0;
    for (let i = -1; i <= 1; i++) {
        for (let j = -1; j <= 1; j++) {
            if (i === 0 && j === 0) continue;
            let nx = (x + i + gridWidth) % gridWidth;
            let ny = (y + j + gridHeight) % gridHeight;
            count += grid[nx][ny];
        }
    }
    return count;
}

// Update the click event to account for dynamic cell sizes
canvas.addEventListener('click', function (event) {
    const rect = canvas.getBoundingClientRect();
    const x = Math.floor((event.clientX - rect.left) / cellSize);
    const y = Math.floor((event.clientY - rect.top) / cellSize);

    if (x >= 0 && x < gridWidth && y >= 0 && y < gridHeight) {
        fetch('/toggle_cells', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ x: x, y: y }),
        })
            .then(response => response.json())
            .then(data => {
                data.toggle_cells.forEach(([tx, ty]) => {
                    if (tx >= 0 && tx < gridWidth && ty >= 0 && ty < gridHeight) {
                        grid[tx][ty] = 1;
                        nextGrid[tx][ty] = 1;
                    }
                });
            });
    }
});

function gameLoop(timestamp) {
    if (transitionProgress < transitionDuration) {
        transitionProgress = Math.min(transitionProgress + 16, transitionDuration);
        drawGrid();
    }
    requestAnimationFrame(gameLoop);
}

// Start the Game of Life
init();
requestAnimationFrame(gameLoop);
