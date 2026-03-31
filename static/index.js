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

//Timer Script

let started = false;
let timerInterval = null;

async function toggleTimer() {
  let timer = document.getElementById("timer");
  let timer_btn = document.getElementById("timer_btn");
  let start = Date.now();

  started = !started;

  if (started) {
    timer_btn.textContent = "Stop Timer";
    timerInterval = setInterval(() => {
      let delta = Date.now() - start;
      timer.textContent = (delta / 1000).toFixed(2);
    }, 10);
  } else {
    timer_btn.textContent = "Start Timer";
    //stop timer, clear timing interval
    clearInterval(timerInterval);
    timerInterval = null;

    let scramble = document.getElementById("scramble").textContent;
    // scramble = scramble.replace(/'/g, "i");
    // scramble = scramble.replace(/ /g, ",");

    //This 'data' variable is what's getting sent to the backend
    const data = {
      scramble: scramble,
      time: timer.textContent,
    };

    await sendSolveToBackend(data);
    await getSolves();
    // zero = 0; // lol
    // timer.textContent = zero.toFixed(2);
    generateScramble();
  }
}

var solves = [];
async function getSolves() {
  try {
    const response = await fetch(`/get_solves/`);
    if (!response.ok) {
      throw new Error(`Error! Status: ${response.status}`);
    }
    const data = await response.json();

    //'solves' variable is at the top of this .js file.
    //   We populate that array with this line
    solves = data;
    updateUI();

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
    console.error("POST to /solve failed");
  }
}

async function deleteSolve(solveID) {
  try {
    const response = await fetch(`/delete_solve/${solveID}`, {
      method: "DELETE",
    });
    getSolves();
    updateUI();
  } catch (error) {
    console.error("DELETE to /delete_solve/$solveID$ failed");
  }
}
function updateUI() {
  var last = document.getElementById("last");
  var best = document.getElementById("best");
  var avg3 = document.getElementById("avg3");
  var avg5 = document.getElementById("avg5");
  var avg12 = document.getElementById("avg12");
  var avgAll = document.getElementById("avgAll");
  var solvesTableBody = document.getElementById("solves_tbl_body");

  var lengthSolves = solves.length;

  //Find last and best solve
  if (lengthSolves > 0) {
    last.textContent = solves[0].time_seconds;
    var bestTime = Infinity;
    for (const solve of solves) {
      var solveTime = parseFloat(solve.time_seconds);
      if (solveTime < bestTime) {
        bestTime = solveTime;
      }
    }
    best.textContent = bestTime;
  } else {
    last.textContent = "--";
    best.textContent = "--";
  }

  avg3.textContent = calculateSolveAvg(solves, 3);
  avg5.textContent = calculateSolveAvg(solves, 5);
  avg12.textContent = calculateSolveAvg(solves, 12);
  avgAll.textContent = calculateSolveAvg(solves, solves.length);

  // create solves table
  solvesTableBody.innerHTML = "";
  for (let i = 0; i < solves.length; i++) {
    const tr = document.createElement("tr");

    tr.innerHTML = `
    <td>${solves.length - i}</td>
    <td>${solves[i].scramble}</td>
    <td>${solves[i].time_seconds}</td>
    <td><button onclick="deleteSolve(${solves.length - i})" > X </button></td>
    `;

    solvesTableBody.appendChild(tr);
  }
}

function calculateSolveAvg(arr, num) {
  if (arr.length >= num) {
    var sum = 0;
    for (let i = 0; i < num; i++) {
      sum += parseFloat(arr[i].time_seconds);
    }
    sum /= num;
    return sum.toFixed(2);
  } else {
    return "--";
  }
}

getSolves();
generateScramble();
