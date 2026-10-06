.PHONY: help run clean
help:
	@echo "make run | make clean"
run:
	python3 week1_basics/day08_for_loop.py
clean:
	find . -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
