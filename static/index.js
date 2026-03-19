function generateScramble() {
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

  // Build an alternate scramble string which is easier to read for display on the frontend.

  displayedScramble = String(newScramble);
  displayedScramble = displayedScramble.replace(/,/g, " ");

  let scramble = document.getElementById("scramble");
  scramble.textContent = displayedScramble;
}
generateScramble();

//Timer Script

let started = false;
let timerInterval = null;

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
    //stop timer, clear timing interval
    clearInterval(timerInterval);
    timerInterval = null;

    let scramble = document.getElementById("scramble").textContent;
    scramble = scramble.replace(/'/g, "i");
    scramble = scramble.replace(/ /g, ",");

    //This 'data' variable is what's getting sent to the backend
    const data = {
      scramble: scramble,
      time: timer.textContent,
    };

    sendSolveToBackend(data);

    // zero = 0; // lol
    // timer.textContent = zero.toFixed(2);
    generateScramble();
  }
}

var solves = [];
async function getSolves(num) {
  try {
    const response = await fetch(`/get_solves/${num}`);
    if (!response.ok) {
      throw new Error(`Error! Status: ${response.status}`);
    }
    const data = await response.json();

    solves = data;
    console.log("solves: ", solves);
    return solves;
  } catch (error) {
    console.error("Could not get solves: ", error);
  }
}

async function sendSolveToBackend(data) {
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
