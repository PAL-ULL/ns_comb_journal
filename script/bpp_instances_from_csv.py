import pandas as pd
import numpy as np
import sys


file = sys.argv[1]
df = pd.read_csv(file, header=0)

print(df.head().to_numpy())
for i, instance in enumerate(df.to_numpy()):
    filename = f"instance_kevin_{i}_for_{instance[-1]}.bpp"
    content = f"120 150\n\n" + "\n".join(str(v) for v in instance[0:-1])
    with open(filename, "w") as f:
        f.write(content)
