import numpy as np
import math
from scipy.optimize import curve_fit

def log_func(x, a, b, c):
    return a - b * np.log(x + c)

def log_model_predict(x, y):
    X = np.array(x)
    Y = np.array(y)
    fit = curve_fit(log_func, X, Y)
    return log_func(X, *fit[0])

def find_closest_value(x, arg):
    difference = abs(x[0] - arg)
    index = 0

    for i in range(1, len(x)):
        dif = abs(x[i] - arg)
        if dif < difference:
            difference = dif
            index = i

    return index

def get_prediction_for_arg(x, y, arg):
    prediction = log_model_predict(x, y)
    
    value = prediction[find_closest_value(x, arg)]

    if value < 1:
        return 1
    elif value > 20:
        return 20
    else:
        return round(value)