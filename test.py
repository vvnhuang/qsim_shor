import cirq
import qsimcirq

# Define qubits and a short circuit.
q0, q1 = cirq.LineQubit.range(2)
circuit = cirq.Circuit(cirq.H(q0), cirq.CX(q0, q1), cirq.CX(q0,q1))
print("Circuit:")
print(circuit)
print()

# Simulate the circuit with Cirq and return the full state vector.
print('Cirq results:')
cirq_simulator = cirq.Simulator()
cirq_results = cirq_simulator.simulate(circuit)
print(cirq_results)
print()

# Simulate the circuit with qsim and return the full state vector.
print('qsim results:')
qsim_simulator = qsimcirq.QSimSimulator()
qsim_results = qsim_simulator.simulate(circuit)
print(qsim_results)

samples = cirq.sample_state_vector(
    qsim_results.state_vector(), indices=[0, 1], repetitions=10)
print(samples)

import time

# Get a rectangular grid of qubits.
qubits = cirq.GridQubit.rect(4, 5)

# Generates a random circuit2 on the provided qubits.
circuit2 = cirq.experiments.random_rotations_between_grid_interaction_layers_circuit(
    qubits=qubits, depth=16)

# Simulate the circuit2 with Cirq and print the runtime.
cirq_simulator = cirq.Simulator()
cirq_start = time.time()
cirq_results = cirq_simulator.simulate(circuit2)
cirq_elapsed = time.time() - cirq_start
print(f'Cirq runtime: {cirq_elapsed} seconds.')
print()

# Simulate the circuit2 with qsim and print the runtime.
qsim_simulator = qsimcirq.QSimSimulator()
qsim_start = time.time()
qsim_results = qsim_simulator.simulate(circuit2)
qsim_elapsed = time.time() - qsim_start
print(f'qsim runtime: {qsim_elapsed} seconds.')
