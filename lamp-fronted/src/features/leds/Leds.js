import React, { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { selectRgb, updateLedsAction } from "./ledsSlice";
import styles from "./Leds.module.css";
import { ChromePicker, CirclePicker } from "react-color";

export function Leds() {
  const rgb = useSelector(selectRgb);
  const dispatch = useDispatch();
  const [localRgb, setLocalRgb] = useState({ r: rgb[0], g: rgb[1], b: rgb[2] });

  const onChangeColor = color => {
    const { r, g, b } = color.rgb;
    dispatch(updateLedsAction([r, g, b]));
    setLocalRgb({ r, g, b });
  };

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
