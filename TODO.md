# TODO: Optimize parte1.ipynb

- [ ] Add timing imports (time module) and measure load time before and after optimizations.
- [ ] Replace pandas read_csv loop with Dask for parallel reading and concatenation.
- [ ] After loading, optimize data types using astype to downcast integers and floats.
- [ ] Ensure active_cases calculation is vectorized (already is).
- [ ] Add documentation cells with evidence of improvements (times, memory usage).
- [ ] Test the optimized code and verify results.
