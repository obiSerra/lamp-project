import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { updateLeds } from './ledsApi';

const initialState = {
  rgb: [0,0,0],
  status: 'idle',
};

export const updateLedsAction = createAsyncThunk(
  'leds/update',
  async (newRgb) => {
    const response = await updateLeds(newRgb);
    // The value we return becomes the `fulfilled` action payload
    return response.data;
  }
);

export const ledsSlice = createSlice({
  name: 'leds',
  initialState,
  // The `reducers` field lets us define reducers and generate associated actions
  reducers: {
    setRgb: (state, action) => {
      state.rgb = action.payload;
    },
  },
  // The `extraReducers` field lets the slice handle actions defined elsewhere,
  // including actions generated by createAsyncThunk or in other slices.
  extraReducers: (builder) => {
    builder
      .addCase(updateLedsAction.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(updateLedsAction.fulfilled, (state, action) => {
        state.status = 'idle';
        state.rgb = action.payload.rgb;
      });
  },
});

export const { setRgb } = ledsSlice.actions;

// The function below is called a selector and allows us to select a value from
// the state. Selectors can also be defined inline where they're used instead of
// in the slice file. For example: `useSelector((state: RootState) => state.counter.value)`
export const selectRgb = (state) => state.leds.rgb;

// We can also write thunks by hand, which may contain both sync and async logic.
// Here's an example of conditionally dispatching actions based on current state.
// export const incrementIfOdd = (amount) => (dispatch, getState) => {
//   const currentValue = selectRgb(getState());
//   if (currentValue % 2 === 1) {
//     dispatch(setRgb(amount));
//   }
// };

export default ledsSlice.reducer;