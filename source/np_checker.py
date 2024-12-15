try:
    import numpy as np
    print("NumPy version:", np.__version__)
except ImportError as e:
    print("Failed to import NumPy:", e)