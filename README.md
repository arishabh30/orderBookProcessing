# Order Book Processing 
----------
### To run the code on your system with all the required packages installed: 
1. Ensure that python is installed on your system:
    - For Windows : In CMD, type `python3 -version`
    - For Ubuntu : In the terminal, type `python3 --version`
If the output after entering the command is the version of Python installed on your system then proceed forward, otherwise install Python first.       
2. To install all the necessary dependencies: 
    - Run this command to install the *pipreqs* library : `pip install pipreqs`
    - After successful installation, run the command : `pipreqs` in your terminal. This will create a `requirements.txt` file in the existing directory
    - Now run the command `pip install -r requirements.txt` to install all the necessary dependecies
3. Add the file **orders.xml** to the current directory
4. In your terminal execute the code using the command `python3 orderBookProcessing.py`

## Complexity Analysis
The functions mainly determine the time complexity of the code:
1. Adding an Order (`process_add_order`): In the worst case, the code iterates through
the existing orders in the book, which can be **O(n**), where n is the number of existing
orders in the book. The code also sorts the order book based on price and order_id.
Sorting a list of n elements typically has a time complexity of **O(n log n)** due to
sorting.
2. Deleting an Order(`process_delete_order`): The code iterates through the existing
orders in the book, which can be **O(n)**, where n is the number of existing orders in
the book.
3. Overall, the time complexity of the code for adding and deleting orders, as well as
maintaining the order book, is dominated by the sorting operation **(O(n log n))** and
the linear traversal of orders **(O(n))** within the order book.

The code can be optimized by using data structures like Priority Queues (heap) to avoid the
need to sort th elements of the list each time an order message is read.

We can also use multithreading to parallelize the order processing. Each order message can
be processed concurrently.





