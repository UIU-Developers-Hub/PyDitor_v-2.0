# File: backend/run_coverage.sh
#!/bin/bash
# Unix shell script to run coverage
pytest --cov=app --cov-report=term-missing --cov-report=html
if [ $? -eq 0 ]; then
    echo "Opening coverage report..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open coverage_html/index.html
    else
        xdg-open coverage_html/index.html
    fi
fi