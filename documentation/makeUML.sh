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

pyreverse3 -AS ../Tomasulo.py
dot -Tpng classes.dot>./UML/Hierarchy.png

rm *.dot

