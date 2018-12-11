#!/bin/bash
echo "Generating UML..."

cd ..

pyreverse3 Tomasulo.py
dot -Tpng classes.dot> documentation/UML/Tomasulo.png

pyreverse3 src/IntegerALU.py
dot -Tpng classes.dot> documentation/UML/IntegerALU.png

pyreverse3 src/InstructionQueue.py
dot -Tpng classes.dot> documentation/UML/InstructionQueue.png

pyreverse3 src/ROB.py
dot -Tpng classes.dot> documentation/UML/ROB.png

pyreverse3 src/FPALU.py
dot -Tpng classes.dot> documentation/UML/FPALU.png

pyreverse3 src/MemoryUnit.py
dot -Tpng classes.dot> documentation/UML/MemoryUnit.png

pyreverse3 src/RAT.py
dot -Tpng classes.dot> documentation/UML/RAT.png

pyreverse3 src/ARF.py
dot -Tpng classes.dot> documentation/UML/ARF.png

pyreverse3 src/BranchUnit.py
dot -Tpng classes.dot> documentation/UML/BranchUnit.png

pyreverse3 src/LdStQ.py
dot -Tpng classes.dot> documentation/UML/LdStQ.png

pyreverse3 -AS Tomasulo.py
dot -Tpng classes.dot> documentation/UML/Hierarchy.png

rm *.dot

