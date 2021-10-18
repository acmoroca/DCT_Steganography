# Adapted from slides presented by Bernd Girod
import math

# ---- Constants ----

C = [math.cos(math.pi / 16 * i) for i in range(8)]
S = [1 / (4 * val) for val in C]
S[0] = 1 / (2 * math.sqrt(2))
A = [
	None,
	C[4],
	C[2] - C[6],
	C[4],
	C[6] + C[2],
	C[6],
]

def transform(vector):
	v0 = vector[0] + vector[7]
	v1 = vector[1] + vector[6]
	v2 = vector[2] + vector[5]
	v3 = vector[3] + vector[4]
	v4 = vector[3] - vector[4]
	v5 = vector[2] - vector[5]
	v6 = vector[1] - vector[6]
	v7 = vector[0] - vector[7]

	v8 = v0 + v3
	v9 = v1 + v2
	v10 = v1 - v2
	v11 = v0 - v3
	v12 = -v4 - v5
	v13 = (v5 + v6) * A[3]
	v14 = v6 + v7

	v15 = v8 + v9
	v16 = v8 - v9
	v17 = (v10 + v11) * A[1]
	v18 = (v12 + v14) * A[5]

	v19 = -v12 * A[2] - v18
	v20 = v14 * A[4] - v18

	v21 = v17 + v11
	v22 = v11 - v17
	v23 = v13 + v7
	v24 = v7 - v13

	v25 = v19 + v24
	v26 = v23 + v20
	v27 = v23 - v20
	v28 = v24 - v19

	return [
		S[0] * v15,
		S[1] * v26,
		S[2] * v21,
		S[3] * v28,
		S[4] * v16,
		S[5] * v25,
		S[6] * v22,
		S[7] * v27,
	]

def inverse_transform(vector):
	v15 = vector[0] / S[0]
	v26 = vector[1] / S[1]
	v21 = vector[2] / S[2]
	v28 = vector[3] / S[3]
	v16 = vector[4] / S[4]
	v25 = vector[5] / S[5]
	v22 = vector[6] / S[6]
	v27 = vector[7] / S[7]

	v19 = (v25 - v28) / 2
	v20 = (v26 - v27) / 2
	v23 = (v26 + v27) / 2
	v24 = (v25 + v28) / 2

	v7  = (v23 + v24) / 2
	v11 = (v21 + v22) / 2
	v13 = (v23 - v24) / 2
	v17 = (v21 - v22) / 2

	v8 = (v15 + v16) / 2
	v9 = (v15 - v16) / 2

	v18 = (v19 - v20) * A[5]
	v12 = (v19 * A[4] - v18) / (A[2] * A[5] - A[2] * A[4] - A[4] * A[5])
	v14 = (v18 - v20 * A[2]) / (A[2] * A[5] - A[2] * A[4] - A[4] * A[5])

	v6 = v14 - v7
	v5 = v13 / A[3] - v6
	v4 = -v5 - v12
	v10 = v17 / A[1] - v11

	v0 = (v8 + v11) / 2
	v1 = (v9 + v10) / 2
	v2 = (v9 - v10) / 2
	v3 = (v8 - v11) / 2

	return [
		(v0 + v7) / 2,
		(v1 + v6) / 2,
		(v2 + v5) / 2,
		(v3 + v4) / 2,
		(v3 - v4) / 2,
		(v2 - v5) / 2,
		(v1 - v6) / 2,
		(v0 - v7) / 2,
	]
