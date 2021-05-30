from tasks import add
import time

result = add.delay(10, 20)
print(result.ready())
time.sleep(2)
print(result.get(timeout=1))
print(result.ready())
print(result.forget())
