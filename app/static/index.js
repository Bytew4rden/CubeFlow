var numSolves = 1;

function incrSolves() {
  numSolves++;
}

function generateScramble() {
  let scramble = document.getElementById("scramble");

  const layers = ["U", "D", "L", "R", "F", "B"];
  const moveTypes = ["", "'", "2"];
  const possibleNextLayers = {
    U: ["L", "R", "F", "B"],
    D: ["L", "R", "F", "B"],
    L: ["U", "D", "F", "B"],
    R: ["U", "D", "F", "B"],
    F: ["U", "D", "L", "R"],
    B: ["U", "D", "L", "R"],
  };

  let newScramble = [];

  let prevLayer = layers[Math.floor(Math.random() * layers.length)];
  let prevMoveType = moveTypes[Math.floor(Math.random() * moveTypes.length)];

  newScramble.push(prevLayer + prevMoveType);

  for (let i = 0; i < 19; i++) {
    let possibleNexts = possibleNextLayers[prevLayer];
    let next = possibleNexts[Math.floor(Math.random() * possibleNexts.length)];
    let moveType = moveTypes[Math.floor(Math.random() * moveTypes.length)];
    prevLayer = next;

    newScramble.push(next + moveType);
  }

  scramble.textContent = newScramble.join(" ");
}
generateScramble();

//Timer Script

let started = false;
let timerInterval = null;
let solves = [];

function toggleTimer() {
  let timer = document.getElementById("timer");
  let start = Date.now();

  started = !started;

  if (started) {
    timerInterval = setInterval(() => {
      let delta = Date.now() - start;
      timer.textContent = Math.floor(delta / 1000);
    }, 1000);
  } else {
    clearInterval(timerInterval);
    timerInterval = null;

    let scramble = document.getElementById("scramble").textContent;
    let data = String(
      numSolves + ": " + scramble + " | Time:" + timer.textContent + "s",
    );

    solves.push(timer.textContent);

    let solveDiv = document.getElementById("solves");

    let newSolveDiv = document.createElement("div");

    newSolveDiv.textContent = data;

    solveDiv.appendChild(newSolveDiv);

    incrSolves();
    timer.textContent = 0;
    generateScramble();
  }
}
