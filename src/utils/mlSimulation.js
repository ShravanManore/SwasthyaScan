export const runMLSimulation = async (onStepUpdate, delay = 1000) => {
  for (let index = 0; index < 6; index += 1) {
    onStepUpdate(index, 'running');
    await new Promise((resolve) => setTimeout(resolve, delay));
    onStepUpdate(index, 'completed');
  }
};
