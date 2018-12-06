# Tomasulo-Softcore
This is our project submission for a single-core soft CPU running Tomasulo's Algorithm with re-ordering buffers, speculative execution, and memory disambiguation.  This work was prepared for the graduate-level computer architecture course, ECE2162, at the University of Pittsburgh.

# Software Requirements
The project assumes you are running a terminal with Python 3.6+ in the CLI path and execution privileges.  To generate new UML images using the makeUML script, you will need graphviz and pylint3 installed and available in your path.

# Build Instructions
To run the project with a test input, type:
`<python 3> Tomasulo.py test1.txt`
where <python 3> is your python 3 CLI interpreter and test1.txt is a valid input file

# Test Cases
The test cases incrementally test that all instructions are properly supported, that the algorithm is executing correctly, and that the additional features are performing their respective tasks correctly.  The test cases are organized into the testCases/ directory by prefix; "test1.txt", "test1_expected.txt", and "test1_output.txt" designate the input test case file, the hand-derived output expected, and the actual output generated respectively.

To test individual modules in the src directory, run them directly as scripts:
`<python 3> ROB.py`

# Status
- The project is currently under active development
- The project is not in a working state

# Project Requirements
[See here](rubric.md)

# Description of Operation
Our software hierarchy is depicted below in the UML diagram.  To handle the requirement that some functional units are pipelined and others are not, we replicate time-tracking in the subclasses and functional units; cycles are counted and incremented by the top-level Tomasulo class, and for functional units that have time sensitive actions, an advanceTime() function is used to progress by one time unit.

![The class hierarchy UML of the Tomasulo-Softcore](documentation/UML/Hierarchy.png)

# Tasks
## Major Functional Units
- [x] Input Parsing
- [x] ROB class
- [x] RS class
- [x] RAT class
- [x] Integer ALU class
- [x] FP Adder class
- [x] FP Multiplier class
- [x] Instruction Queue class
- [x] Branch Unit class
- [x] Memory Unit class
- [x] Integer Register File
- [x] FP Register File
- [x] Output Generator
- [x] Issue procedure
- [x] Execute procedure
- [x] Memory procedure
- [x] Writeback procedure
- [x] Commit procedure

## Outstanding Test Cases
- [ ] Simple ISA test case: Load/Store end-to-end
- [ ] Addressing corner cases test
- [ ] Verify absence of WAR test case
- [ ] Verify memory disambiguation
- [ ] Complex test case: write patterns to memory
- [ ] Complex test case: sum over floats in memory


