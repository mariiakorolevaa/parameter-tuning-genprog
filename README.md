This project generates the most suitable hyperparameters for GenProg algorithm in Whisker program repair. 

There are two different modes of generation:
1. **Integer mode.** Generates the population size and elitism size.

2. **Float mode.** Generates the probability of mutation and crossover. Headless execution of the program repair: genetation of mutation rate and crossover rate. Full execution of the program repair: genenation of mutation insertion rate, mutation change rate, mutation deletion rate, crossover rate.

The script chooses the best hyperparameters depending on the quality of the solution (its fitness value) and execution time.  

Possible parameters to run the script:
```
--is_rationals - to generate float values (muatation and crossover rate)
--mode - rs or de. To choose a mode of the parameter tuning. RS means random search. DE means differential evolution. 
--n_jobs - a number of parallel tasks. 
--is_headless - to run Whisker program repair without opening browser windows. 
--acceleration_factor
--path_to_repair - a path to a Scratch program you want to repair. 
--path_to_test - a path to a file with tests which will assess the quality of the solution (repaired program).
--path_to_output - a path to the repaired program.
--path_to_csv - a path to a CSV file with results of searching the solution. 
--path_to_config - a path to a configuration file of a Whisker project. 
--whisker_path - a path to the Whisker project folder.
--population_size - how many populations to generate while looking for a tuning parameters.
--max_iter - max. number of iterations.
```



External libraries used in the project are presented in **requirements.txt** file:

    pandas~=2.1.1
    numpy~=1.26.0
    scipy~=1.11.3
    joblib~=1.2.0
    tabulate~=0.9.0

To install all Python requirements:

    pip install -r requirements.txt
