
```bash
pip install --user -e .
cd special_cases
python3 1_before.py
...
```

Doesn't work yet: 2, 5.


Issues:
1. Import before patching creates direct pointer to module, bypass patched module.
