import numpy as np
import pandas as pd
import selenium
import requests

def main() -> None:
    print("entrypoint active")
    print("numpy:", np.__version__)
    print("pandas:", pd.__version__)
    print("selenium:", selenium.__version__)
    print("requests:", requests.__version__)

if __name__ == "__main__":
    main()