import React from 'react'
import styles from './Drone.module.css'

function Drone() {
  return (
    <>
      <div className={styles.drone}></div>
      <div className={styles.tree}>
        <div className={styles.foliage}></div>
      </div>

      <div className={styles.button_container}>
        <h1>Run Python Script</h1>
        <input id="detect" type="text" placeholder="Status" />
        <button className="btn" onClick={() => {run_python_test()}}>Run</button>
      </div>

      <div className="python output">
        <div id="output" className={styles.output_box}>Script Output</div>
      </div>
    </>
  )
}

export default Drone