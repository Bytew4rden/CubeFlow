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
      timer.textContent = (delta / 1000).toFixed(2);
    }, 10);
  } else {
    clearInterval(timerInterval);
    timerInterval = null;

    let scramble = document.getElementById("scramble").textContent;

    //This 'data' variable is what's getting sent to the backend
    const data = {
      scramble: String(scramble),
      time: String(timer.textContent),
    };

    //reset UI, generating a new scramble
    zero = 0;
    timer.textContent = zero.toFixed(2);
    generateScramble();

    sendDataToBackend(data);
  }
}

async function sendDataToBackend(data) {
  try {
    const response = await fetch("/solve", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
  } catch (error) {
    console.error("POST to /solve failure");
  }
}
