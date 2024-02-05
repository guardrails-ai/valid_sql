# to run these, run 
# pytest test/test-validator.py

from guardrails import Guard
from validator import ValidSQL

# We use 'refrain' as the validator's fail action,
#  so we expect failures to always result in a guarded output of None
# Learn more about corrective actions here:
#  https://www.guardrailsai.com/docs/concepts/output/#%EF%B8%8F-specifying-corrective-actions
guard = Guard.from_string(validators=[ValidSQL(on_fail="refrain")])

def test_pass():
  test_output = "SELECT name, age FROM users WHERE age > 18;"
  raw_output, guarded_output, *rest = guard.parse(test_output)
  assert(guarded_output is test_output)

def test_fail():
  test_output = "SELEC name, age FROMM users WHER age > 18"
  raw_output, guarded_output, *rest = guard.parse(test_output)
  assert(guarded_output is None)
