import React from 'react'

function Drone() {
  return (
    <>
      <div class="drone"></div>
      <div class="tree">
        <div class="foliage"></div>
      </div>

      <div class="button-container">
        <h1>Run Python Script</h1>
        <input id="detect" type="text" placeholder="Status" />
        <button class="btn btn-success" onclick="run_python_test()">Run</button>
      </div>

      <div class="python output">
        <div id="output" class="output_box">Script Output</div>
      </div>
    </>
  )
}

export default Drone