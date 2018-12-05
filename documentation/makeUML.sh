#!/bin/bash
echo "Generating UML..."

pyreverse3 ../Tomasulo.py
dot -Tpng classes.dot>./UML/Tomasulo.png

pyreverse3 ../src/IntegerALU.py
dot -Tpng classes.dot>./UML/IntegerALU.png

pyreverse3 ../src/InstructionQueue.py
dot -Tpng classes.dot>./UML/InstructionQueue.png

pyreverse3 ../src/ROB.py
dot -Tpng classes.dot>./UML/ROB.png

pyreverse3 ../src/FPALU.py
dot -Tpng classes.dot>./UML/FPALU.png

pyreverse3 ../src/MemoryUnit.py
dot -Tpng classes.dot>./UML/MemoryUnit.png

pyreverse3 ../src/RAT.py
dot -Tpng classes.dot>./UML/RAT.png

pyreverse3 ../src/ARF.py
dot -Tpng classes.dot>./UML/ARF.png

pyreverse3 ../src/BranchUnit.py
dot -Tpng classes.dot>./UML/BranchUnit.png

pyreverse3 -AS ../Tomasulo.py
dot -Tpng classes.dot>./UML/Hierarchy.png

rm *.dot

