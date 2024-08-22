from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.number import inverse
import cirq
import numpy as np
import random
import math
import time
 
def qft(circuit, qubits):
    """Quantum Fourier Transform."""
    n = len(qubits)
    for i in range(n):
        for j in range(i + 1, n):
            circuit.append(cirq.CZ(qubits[j], qubits[i]) ** (1 / 2 ** (j - i)))
        circuit.append(cirq.H(qubits[i]))
 
def qpe(a, N):
    """Quantum Phase Estimation."""
    num_qubits = int(np.ceil(np.log2(N))) # 4
    qubits = cirq.LineQubit.range(num_qubits * 2) # 8 bits
    circuit = cirq.Circuit()
    # Apply Hadamard gates
    for i in range(num_qubits):
        circuit.append(cirq.H(qubits[i]))
    # Apply controlled-U operations
    for i in range(num_qubits):
        power = 2 ** i
        for j in range(num_qubits):
            circuit.append(cirq.CZ(qubits[i], qubits[num_qubits + j]) ** (a ** power % N))
    qft(circuit, qubits[:num_qubits])

    # Measurement
    circuit.append(cirq.measure(*qubits[:num_qubits]))
    # print(circuit)
 
    return circuit
 
def run_simulation(circuit):
    """Simulate the quantum circuit."""
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1)
    return result

def get_measurement_result_decimal(result):
    measurement_bits = []
    for key in sorted(result.measurements.keys()):
        bits = result.measurements[key][0]
        measurement_bits.extend([str(bit) for bit in bits])
    result_str = ''.join(measurement_bits)
    result_int = int(result_str, 2)
    
    return result_int

def cf(y, N):
    num_qubits = int(np.ceil(np.log2(N)))
    Q = 1 << (num_qubits*2)-1
    fractions = []
    while Q != 0:
        fractions.append(y // Q)
        tA = y % Q
        y = Q
        Q = tA
    depth = 2

    def partial(fractions, depth):
        c = 0
        r = 1

        for i in reversed(range(depth)):
            tR = fractions[i] * r + c
            c = r
            r = tR

        return c

    r = 0
    for d in range(depth, len(fractions) + 1):
        tR = partial(fractions, d)
        if tR == r or tR >= N:
            return r
        r = tR
    return r

# Modular Exponentiation
def modExp(a, exp, mod):
	fx = 1
	while exp > 0:
		if (exp & 1) == 1:
			fx = fx * a % mod
		a = (a * a) % mod
		exp = exp >> 1

	return fx

def checkCandidates(a, r, N, neighborhood):
	if r is None:
		return None

	# Check multiples
	for k in range(1, neighborhood + 2):
		tR = k * r
		if modExp(a, a, N) == modExp(a, a + tR, N):
			return tR

	# Check lower neighborhood
	for tR in range(r - neighborhood, r):
		if modExp(a, a, N) == modExp(a, a + tR, N):
			return tR

	# Check upper neigborhood
	for tR in range(r + 1, r + neighborhood + 1):
		if modExp(a, a, N) == modExp(a, a + tR, N):
			return tR

	return None

def shors_algorithm(N, neighborhood=0.01):
    """Shor's algorithm implementation."""
    attempts=40
    neighborhood = math.floor(N * neighborhood) + 1
    periods = []

    for attempt in range(attempts):
        # print("\nAttempt #" + str(attempt))
        #find a suitable number g satisfies gcd(g,N)==1
        a = random.randint(2, N - 1)
        while np.gcd(a, N) != 1:
            a = random.randint(2, N - 1)

         #find period()
        circuit = qpe(a, N)

        result = run_simulation(circuit)

        result_num = get_measurement_result_decimal(result)

        r = cf(result_num, N)
        r = checkCandidates(a, r, N, neighborhood)
        
        if r is None:
            continue

        if (r % 2) > 0:
            continue

        d = modExp(a, (r // 2), N)
        if r == 0 or d == (N - 1):
            continue

        periods.append(r)
        if(len(periods) < 1):
            continue

        r = 1
        for period in periods:
            d = np.gcd(period, r)
            r = (r * period) // d

        b = modExp(a, (r // 2), N)
        if(b==1):
            continue
        f1 = np.gcd(N, b + 1)
        f2 = np.gcd(N, b - 1)

        end = [f1, f2]

        return end
    
    return None

if __name__ == '__main__':
    start_time = time.time()
    # key = RSA.generate(1024)
    # private_key = key.export_key()  # 导出私钥
    # public_key = key.publickey().export_key()  # 导出公钥

    # 假设的模数 n 和公钥指数 e
    n = 33043 #key.n  # 示例值，实际值应为1024位的RSA模数
    e = 65537 #key.e    # 示例公钥指数

    #质因数分解得到的 p 和 q
    result = shors_algorithm(n, 0.01)
    if result is not None:
        print("---------------------------------------------------Factors:", result[0],result[1])
        p = int(result[0])
        q = int(result[1])
        print(p,q)
        # # 计算欧拉函数
        # phi_n = (p - 1) * (q - 1)

        # # 计算私钥指数 d
        # d = inverse(e, phi_n)

        # # 创建 RSA 密钥对象
        # key = RSA.construct((n, e, d))
        # print(key)

        # # 打印私钥
        # print("Private Key:")
        # print(key.export_key().decode())

        # # 加密和解密测试
        # message = b"Hi"
        # cipher_rsa = PKCS1_OAEP.new(key.publickey())
        # ciphertext = cipher_rsa.encrypt(message)

        # print("\nEncrypted message:")
        # print(ciphertext)

        # # 使用私钥解密
        # cipher_rsa = PKCS1_OAEP.new(key)
        # decrypted_message = cipher_rsa.decrypt(ciphertext)

        # print("\nDecrypted message:")
        # print(decrypted_message.decode())
    end_time = time.time()

    run_time = end_time - start_time
    print(f"RUN time: {run_time:-4f} seconds")



