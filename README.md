# Tomasulo-Softcore
This is our project submission for a single-core soft CPU running Tomasulo's Algorithm with re-ordering buffers, speculative execution, and memory disambiguation.  This work was prepared for the graduate-level computer architecture course, ECE2162, at the University of Pittsburgh.

# Software Requirements
The project assumes you are running a terminal with Python 3.6+ in the CLI path and execution privileges.
[![Updates](https://pyup.io/repos/github/SLongofono/Tomasulo-Softcore/shield.svg)](https://pyup.io/repos/github/SLongofono/Tomasulo-Softcore/)

# Build Instructions
To run the project with a test input, type:
`<python 3> Tomasulo.py test1.txt`
where <python 3> is your python 3 CLI interpreter and test1.txt is a valid input file

# Test Cases
The test cases incrementally test that all instructions are properly supported, that the algorithm is executing correctly, and that the additional features are performing their respective tasks correctly.  The test cases are organized into the tests directory by prefix; test1_input.txt and test1_expected.txt designate the input test case file and the hand-derived output expected for that test case.

To test individual modules in the src directory, run them directly as scripts:
`<python 3> ROB.py`

# Tasks
## Major Functional Units 
- [x] Input Parsing
- [x] ROB class
- [ ] RS class
- [ ] Integer ALU class
- [ ] FP Adder class
- [ ] FP Multiplier class
- [ ] Instruction Queue class
- [ ] Branch Unit class
- [ ] Memory Unit class

## Test Cases
- [ ] Simple ISA test case: ALU
- [ ] Simple ISA test case: FPALU
- [ ] Simple ISA test case: FP Multiplier
- [ ] Simple ISA test case: Load/Store
- [ ] Simple ISA test case: Branch
- [ ] Addressing corner test cases
- [ ] Verify absence of WAW test case
- [ ] Verify absence of WAR test case
- [ ] Verify handling of RAW test case
- [ ] Verify memory disambiguation
- [ ] Verify illegal instructions fail
- [ ] Complex test case: all instructions
- [ ] Complex test case: Fibonacci numbers
- [ ] Complex test case: extended length loop
- [ ] Complex test case: write patterns to memory

# Project Requirements
[See here](../rubric.md)

# Description of Operation
The overview is here.
