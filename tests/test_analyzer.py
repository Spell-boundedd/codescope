from codescope.analyzer import analyze_project

def test_analyzer_runs():

```
result = analyze_project(".")

assert result is not None
assert "total_files" in result
```
