# Tomasulo-Softcore
This is our project submission for a single-core soft CPU running Tomasulo's Algorithm with re-ordering buffers, speculative execution, and memory disambiguation.  This work was prepared for the graduate-level computer architecture course, ECE2162, at the University of Pittsburgh.

# Status
The project is under development, and this is only a skeleton.
[![Updates](https://pyup.io/repos/github/SLongofono/Tomasulo-Softcore/shield.svg)](https://pyup.io/repos/github/SLongofono/Tomasulo-Softcore/)

# Requirements
The project assumes you are running a terminal with Python 3.6+ and execution privileges.

# Build Instructions
To build the project, do this.
`python3 tomasulo.py test1`

To test the project, do that.

# Test Cases
The test cases incrementally test that all instructions are properly supported, that the algorithm is executing correctly, and that the additional features are performing their respective tasks correctly.  The test cases are organized into the tests directory by prefix; test1_input.txt and test1_expected.txt designate the input test case file and the hand-derived output expected for that test case.

# Description of Operation
The overview is here.
