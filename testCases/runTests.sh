#!/bin/bash
set -o pipefail
# Runs all test cases
echo "Running test suite..."

NUMTESTS=11
TESTSPASSED=0

echo "Simple test 1..."
python3 ../Tomasulo.py simple1.txt >/dev/null 2>&1
RESULT="$(diff simple1_expected.txt simple1_output.txt | wc -l)"
if [[ $? -ne 0 ]]
then
	echo "FAIL"
	echo "INCOMPLETE TEST"
elif [[ $RESULT -ne 0 ]]
then
	echo "FAIL"
	echo $RESULT
else
	echo "PASS"
	TESTSPASSED=$((TESTSPASSED+1))
fi
echo

echo "Simple test 2..."
python3 ../Tomasulo.py simple2.txt >/dev/null 2>&1
RESULT="$(diff simple2_expected.txt simple2_output.txt | wc -l)"
if [[ $? -ne 0 ]]
then
	echo "FAIL"
	echo "INCOMPLETE TEST"
elif [[ $RESULT -ne 0 ]]
then
	echo "FAIL"
	echo $RESULT
else
	echo "PASS"
	TESTSPASSED=$((TESTSPASSED+1))
fi
echo

echo "Simple test 3..."
python3 ../Tomasulo.py simple3.txt >/dev/null 2>&1
RESULT="$(diff simple3_expected.txt simple3_output.txt | wc -l)"
if [[ $? -ne 0 ]]
then
	echo "FAIL"
	echo "INCOMPLETE TEST"
elif [[ $RESULT -ne 0 ]]
then
	echo "FAIL"
	echo $RESULT
else
	echo "PASS"
	TESTSPASSED=$((TESTSPASSED+1))
fi
echo

echo "Simple test 4..."
python3 ../Tomasulo.py simple4.txt >/dev/null 2>&1
RESULT="$(diff simple4_expected.txt simple4_output.txt | wc -l)"
if [[ $? -ne 0 ]]
then
	echo "FAIL"
	echo "INCOMPLETE TEST"
elif [[ $RESULT -ne 0 ]]
then
	echo "FAIL"
	echo $RESULT
else
	echo "PASS"
	TESTSPASSED=$((TESTSPASSED+1))
fi
echo

echo "Simple test 5..."
python3 ../Tomasulo.py simple5.txt >/dev/null 2>&1
RESULT="$(diff simple5_expected.txt simple5_output.txt | wc -l)"
if [[ $? -ne 0 ]]
then
	echo "FAIL"
	echo "INCOMPLETE TEST"
elif [[ $RESULT -ne 0 ]]
then
	echo "FAIL"
	echo $RESULT
else
	echo "PASS"
	TESTSPASSED=$((TESTSPASSED+1))
fi
echo

echo "Simple test 6..."
python3 ../Tomasulo.py simple6.txt >/dev/null 2>&1
RESULT="$(diff simple6_expected.txt simple6_output.txt | wc -l)"
if [[ $? -ne 0 ]]
then
	echo "FAIL"
	echo "INCOMPLETE TEST"
elif [[ $RESULT -ne 0 ]]
then
	echo "FAIL"
	echo $RESULT
else
	echo "PASS"
	TESTSPASSED=$((TESTSPASSED+1))
fi
echo

echo "Simple test 7..."
python3 ../Tomasulo.py simple7.txt >/dev/null 2>&1
RESULT="$(diff simple7_expected.txt simple7_output.txt | wc -l)"
if [[ $? -ne 0 ]]
then
	echo "FAIL"
	echo "INCOMPLETE TEST"
elif [[ $RESULT -ne 0 ]]
then
	echo "FAIL"
	echo $RESULT
else
	echo "PASS"
	TESTSPASSED=$((TESTSPASSED+1))
fi

echo "Simple test 8..."
python3 ../Tomasulo.py simple8.txt >/dev/null 2>&1
RESULT="$(diff simple8_expected.txt simple8_output.txt | wc -l)"
if [[ $? -ne 0 ]]
then
	echo "FAIL"
	echo "INCOMPLETE TEST"
elif [[ $RESULT -ne 0 ]]
then
	echo "FAIL"
	echo $RESULT
else
	echo "PASS"
	TESTSPASSED=$((TESTSPASSED+1))
fi

echo "Simple test 9..."
python3 ../Tomasulo.py simple9.txt >/dev/null 2>&1
RESULT="$(diff simple9_expected.txt simple9_output.txt | wc -l)"
if [[ $? -ne 0 ]]
then
	echo "FAIL"
	echo "INCOMPLETE TEST"
elif [[ $RESULT -ne 0 ]]
then
	echo "FAIL"
	echo $RESULT
else
	echo "PASS"
	TESTSPASSED=$((TESTSPASSED+1))
fi

echo "Complex test 6..."
python3 ../Tomasulo.py complex6.txt >/dev/null 2>&1
RESULT="$(diff complex6_expected.txt complex6_output.txt | wc -l)"
if [[ $? -ne 0 ]]
then
	echo "FAIL"
	echo "INCOMPLETE TEST"
elif [[ $RESULT -ne 0 ]]
then
	echo "FAIL"
	echo $RESULT
else
	echo "PASS"
	TESTSPASSED=$((TESTSPASSED+1))
fi

echo "Complex test 7..."
python3 ../Tomasulo.py complex7.txt >/dev/null 2>&1
RESULT="$(diff complex7_expected.txt complex7_output.txt | wc -l)"
if [[ $? -ne 0 ]]
then
	echo "FAIL"
	echo "INCOMPLETE TEST"
elif [[ $RESULT -ne 0 ]]
then
	echo "FAIL"
	echo $RESULT
else
	echo "PASS"
	TESTSPASSED=$((TESTSPASSED+1))
fi
echo

printf "Tests passed: %d / %d (%d %%)" "$TESTSPASSED" "$NUMTESTS" "$((100*TESTSPASSED/NUMTESTS))"
echo

