// A mock function to mimic making an async request for data

import axios from "axios";

const baseUrl = process.env.REACT_APP_BASE_URL ?? "";

export function updateLeds(rgb = [0, 0, 0]) {
  return axios.post(`${baseUrl}/leds`, {
    rgb,
  });
}


// export function updateLeds(rgb = [0, 0, 0]) {
//   return new Promise(resolve => setTimeout(() => resolve({ data: rgb }), 500));
// }
