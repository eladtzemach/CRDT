# CRDT
Implementation of the LWW (Last-Writer-Wins) CRDT data structure
using Python dictionaries and Redis sorted set (ZSET).

The program was built using: <br />
Language: Python 3.4 <br />
IDE: PyCharm <br />
OS: Windows 8


## Assumptions and Design Choices:

1. Notice the `requirements.txt` file. It only includes `redis==2.10.6` which needs to be installed and run locally. 

2. The `lww.add(..)` and `lww.remove(..)` functions always return `True` which means the operation was successfull
(**not** that the element was added/removed).
In a real distributed system environment, this of course may not always be the case and we would have to account for possible
network connection issues / system failure / etc.. and implement a retry/rollback mechanism.

3. When calculating tax, the `calculate_tax()` functions of the `Product` class calls the `calculate_tax()` functions of both
`ProductOrigin` and `ProductCategory` classes since we can have tax of only one of them or both, depends on the product's
category and origin (local vs. imported).
This type of logic helps if in the future we decide to make non-taxable items taxable or vice versa.

4. Just to be safe, `RLock()`s are used when adding/removing elements (not when reading).
This provides us a layer of protection against data race which could occur when dealing with a multi-threaded process.

## Testing:

Aside from manual testing, i have included 16 unit tests for both LWW implementations.
The tests include single-thread and multi-threaded tests.
For running the tests, run `python run_tests.py` from the command prompt / terminal.
Expected output:
```
................
----------------------------------------------------------------------
Ran 16 tests in 0.087s

OK
```
