from sympy import Matrix, eye, simplify, Rational

def expected_steps_to_absorption(target):
    n = target - 2
    """
    n: number of states in the model, including transient states from 3 to target-1,
       and the absorbing state at target. So n = target - 2.
    """
    assert n >= 1, "Need at least one transient state (n >= 1)"

    # Construct full P matrix of size (n+1) x (n+1)
    # States: [3, 4, ..., target-1, target]
    P = []
    for i in range(n + 1):
        row = [0] * (n + 1)

        if i == n:
            row[i] = 1  # absorbing state
        else:
            row[0] = Rational(34, 100)  # restart to state 3
            row[i + 1] = Rational(66, 100)  # step forward
        print(i, row)
        P.append(row)

    P = Matrix(P)

    # Extract Q: (n-1 x n-1) transient submatrix
    Q = P[:n-1, :n-1]

    # Fundamental matrix: N = (I - Q)^(-1)
    I = eye(n - 1)
    N = (I - Q).inv()

    # Expected steps to absorption
    ones = Matrix([1] * (n - 1))
    expected = simplify(N * ones)

    return P, expected

def state_after_k_steps(P, k, start_state_index=0):
    """
    Computes the state distribution after k steps given the transition matrix P and start state index.
    """
    P_k = P**k
    initial = Matrix([1 if i == start_state_index else 0 for i in range(P.shape[0])])
    final_distribution = simplify(P_k * initial)
    return final_distribution

# Example usage
target = 16
P, expected = expected_steps_to_absorption(target)

print(f"Expected steps to absorption from states 3 to {target - 1}:")
for i, val in enumerate(expected):
    print(f"E_{i + 3} = {val} ≈ {float(val):.6f}")

distribution_1000 = state_after_k_steps(P, 10000)

print(f"\nState distribution after 1000 steps starting from state 3:")
for i, prob in enumerate(distribution_1000):
    print(f"State {i + 3}: {prob} ≈ {float(prob):.6f}")
