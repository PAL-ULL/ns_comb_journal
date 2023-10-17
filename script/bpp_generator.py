import numpy as np
from dataclasses import dataclass


@dataclass
class BPPInstance:
    n: int
    capacity: int
    weights: np.array

    def __repr__(self):
        info = f"{self.n} {self.capacity}\n\n"
        for i in range(self.n):
            info += f"{self.weights[i]}\n"
        return info

    def to_file(self, filename: str = None):
        with open(f"{filename}", "w") as file:
            file.write(self.__str__())


def generate_bpp_instance(
    n: int = 50,
    capacity_ratio: float = 0.8,
    lower_bound: int = 1,
    upper_bound: int = 1000,
):
    weights = np.random.uniform(low=lower_bound, high=upper_bound + 1.0, size=n).astype(
        int
    )
    capacity = int(weights.sum() * capacity_ratio)

    return BPPInstance(n, capacity, weights)


if __name__ == "__main__":
    N = 100
    for i in range(N):
        filename = f"BPP_random_instance_{i}.bpp"
        bpp = generate_bpp_instance(50, 0.8, 1, 500)
        bpp.to_file(filename)
