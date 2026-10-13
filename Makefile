.PHONY: help run check clean
help:
	@echo "make run | make check | make clean"
run:
	python3 week2_logic/day08_for_loop/example.py
check:
	find . -name "*.py" -not -path "./.git/*" -exec python3 -m py_compile {} +
clean:
	find . -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
