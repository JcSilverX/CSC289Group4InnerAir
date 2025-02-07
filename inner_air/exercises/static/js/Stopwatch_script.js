let startBtn = document.getElementById('start');
let stopBtn = document.getElementById('stop');
let resetBtn = document.getElementById('reset');
let submitBtn = document.getElementById('submit');
  
let minute = 00;
let second = 00;
let count = 00;
totalMillie = 00;
  
startBtn.addEventListener('click', function () {
    timer = true;
    stopWatch();
});
  
stopBtn.addEventListener('click', function () {
    timer = false;
    document.getElementById('breathHoldTotalSeconds').value = totalMillie;
});
  
resetBtn.addEventListener('click', function () {
    timer = false;
    minute = 0;
    second = 0;
    count = 0;
    document.getElementById('min').innerHTML = "00";
    document.getElementById('sec').innerHTML = "00";
    document.getElementById('count').innerHTML = "00";
    document.getElementById('breathHoldTotalSeconds').value = "00";
});


function show() {
    document.getElementById('submitHold').style.display="inline-block"
}

function hide() {
    document.getElementById('submitHold').style.display="none"
}

function stopWatch() {
    if (timer) {
        count++;
        totalMillie++;

  
        if (count == 100) {
            second++;
            count = 0;
        }
  
        if (second == 60) {
            minute++;
            second = 0;
        }
  
        if (minute == 60) {
            minute = 0;
            second = 0;
        }
  
        let minString = minute;
        let secString = second;
        let countString = count;
 
        if (minute < 10) {
            minString = "0" + minString;
        }
  
        if (second < 10) {
            secString = "0" + secString;
        }
  
        if (count < 10) {
            countString = "0" + countString;
        }
  
        document.getElementById('min').innerHTML = minString;
        document.getElementById('sec').innerHTML = secString;
        document.getElementById('count').innerHTML = countString;
        setTimeout(stopWatch, 10);
    }
}
