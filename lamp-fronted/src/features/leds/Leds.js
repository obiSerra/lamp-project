import React, { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { selectRgb, updateLedsAction, getLedsAction, fadeToAction } from "./ledsSlice";
import styles from "./Leds.module.css";
import { ChromePicker, CirclePicker } from "react-color";

import { Button, IconButton, TextField } from "@material-ui/core";
import { ArrowLeft, ArrowRight } from "@material-ui/icons";

export function Leds() {
  const rgb = useSelector(selectRgb);
  const dispatch = useDispatch();

  const [localRgb, setLocalRgb] = useState({ r: rgb[0], g: rgb[1], b: rgb[2] });
  const [typeChange, setTypeChange] = useState("snap");
  const [speed, setSpeed] = useState(5);

  const onChangeColor = color => {
    const { r, g, b } = color.rgb;
    if (typeChange === "snap") {
      dispatch(updateLedsAction([r, g, b]));
    } else if (typeChange === "fade") {
      dispatch(fadeToAction({ rgb: [r, g, b], speed: speed }));
    }

    setLocalRgb({ r, g, b });
  };

  useEffect(() => dispatch(getLedsAction()), [dispatch]);

  useEffect(() => {
    setLocalRgb({ r: rgb[0], g: rgb[1], b: rgb[2] });
  }, [rgb]);

  const presets = [
    "#000000",
    "#ffffff",

    "#ff0000",
    "#00ff00",
    "#0000ff",

    "#320000",
    "#003200",
    "#000032",

    "#640000",
    "#006400",
    "#000064",

    "#f44336",
    "#e91e63",
    "#9c27b0",
    "#673ab7",
    "#3f51b5",
    "#2196f3",
    "#03a9f4",
    "#00bcd4",
    "#009688",
    "#4caf50",
    "#8bc34a",
    "#cddc39",
    "#ffeb3b",
    "#ffc107",
    "#ff9800",
    "#ff5722",
    "#795548",
  ];

  return (
    <div>
      <div className={styles.leds}>
        <h1>Leds color picker</h1>

        <div className={styles.animationBtnContainer}>
          <Button
            className={styles.animationBtn}
            variant={typeChange === "snap" ? "contained" : "outlined"}
            onClick={() => setTypeChange("snap")}
            color="primary"
          >
            Snap
          </Button>
          <Button
            className={styles.animationBtn}
            variant={typeChange === "fade" ? "contained" : "outlined"}
            onClick={() => setTypeChange("fade")}
            color="primary"
          >
            Fade
          </Button>
        </div>

        <div>

          <IconButton aria-label="dec" onClick={() => setSpeed(Math.max(1, speed - 1))}>
            <ArrowLeft />
          </IconButton>

          <TextField className={styles.smallInput} value={speed} onChange={(e) => setSpeed(Math.max(1, Math.min(10, e.target.value)))} />/10
          <IconButton aria-label="inc" onClick={() => setSpeed(Math.min(10, speed + 1))}>
            <ArrowRight />
          </IconButton>
        </div>
        <div className={styles.pickerContainer}>
          <div className={styles.picker}>
            <ChromePicker disableAlpha={true} color={localRgb} onChangeComplete={onChangeColor} />
          </div>
          <div className={styles.picker}>
            <CirclePicker color={localRgb} onChangeComplete={onChangeColor} colors={presets} />
          </div>
        </div>
      </div>
    </div>
  );
}
