import { configureStore } from '@reduxjs/toolkit';
import ledsReducer from '../features/leds/ledsSlice';

export const store = configureStore({
  reducer: {
    leds: ledsReducer,
  },
});
