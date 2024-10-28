// Load data from URL
function loadDefaultData() {
  if (location.hash !== '') {
    const urlList = JSON.parse(atob(location.hash.split('#')[1]))

    document.querySelector('#code-area').value = urlList[0]
    document.querySelector('#output-text').value = urlList[1]
  }
}
loadDefaultData()

// Create and configure a new web worker to run python code
function createCodeWorker() {
  const codeWorker = new Worker('/worker.js')

  codeWorker.addEventListener('message', function (msg) {
    console.log('Message received')

    if (msg.data.type === 'result') {
      document.querySelector('#code-output').innerHTML = msg.data.result
      runButton.disabled = false
      endButton.disabled = true
    }
  })

  return codeWorker
}

// Run python code in web worker and deal with run button
let codeWorker = createCodeWorker()

// get HTML elements
const runButton = document.querySelector('#run-button')
const endButton = document.querySelector('#end-button')
// Ensure the end button is disabled by default
endButton.disabled = true
const timeDisplayP = document.querySelector('#time-displayed')

// Run code when button pressed.
runButton.addEventListener('click', function () {
  const studentCode = document.querySelector('#code-area').value
  runButton.disabled = true
  endButton.disabled = false

  console.log('Posting message')
  codeWorker.postMessage({
    type: 'run',
    language: 'python',
    code: studentCode,
  })
})

endButton.addEventListener('click', function () {
  codeWorker.terminate()
  codeWorker = createCodeWorker() // send in the next worker
  runButton.disabled = false
  endButton.disabled = true
})
