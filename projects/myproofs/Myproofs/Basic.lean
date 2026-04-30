import Mathlib

open BigOperators

/- (by claude) Helper: 2 * ∑_{p<n+1} p = (n+1)*n in ℕ (Gauss, no truncated subtraction) -/
private lemma two_mul_sum_range_succ (n : ℕ) :
    2 * ∑ p ∈ Finset.range (n + 1), p = (n + 1) * n := by
  induction n with
  | zero => simp
  | succ m ih =>
    rw [Finset.sum_range_succ]
    nlinarith

/- (by claude) Helper: sum transformation for inductive step -/
private lemma sum_succ_eq (n : ℕ) :
    ∑ p ∈ Finset.range n, p * (n + 1 - p) =
    ∑ p ∈ Finset.range n, p * (n - p) + ∑ p ∈ Finset.range n, p := by
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro p hp
  have hpn : p < n := Finset.mem_range.mp hp
  have h1 : n + 1 - p = n - p + 1 := by omega
  rw [h1]
  ring

/- (by claude) Helper: n ≤ n^3 for all n -/
private lemma helper_n_le_n3 (n : ℕ) : n ≤ n^3 := by
  cases n with
  | zero => simp
  | succ n =>
    have : 1 ≤ (n + 1)^2 := Nat.one_le_pow 2 _ (by omega)
    nlinarith [Nat.zero_le n]

/- (by claude) Helper: 6 * LHS = n^3 - n, avoids ℕ division -/
private lemma helper_six_mul_sum (n : ℕ) :
    6 * ∑ p ∈ Finset.range n, p * (n - p) = n^3 - n := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [Finset.sum_range_succ, sum_succ_eq]
    have gauss_succ := two_mul_sum_range_succ n
    have hrange_succ : ∑ p ∈ Finset.range (n + 1), p = ∑ p ∈ Finset.range n, p + n := by
      rw [Finset.sum_range_succ]
    have hle : n ≤ n^3 := helper_n_le_n3 n
    have hle2 : n + 1 ≤ (n + 1)^3 := helper_n_le_n3 (n + 1)
    have hsubn : n + 1 - n = 1 := by omega
    rw [hsubn, Nat.mul_one]
    zify [hle, hle2] at *
    linarith [sq_nonneg (n : ℤ)]

lemma lemma4_path_sum (n : ℕ) :
    ∑ p ∈ Finset.range n, p * (n - p) = (n^3 - n) / 6 := by
  have h := helper_six_mul_sum n; omega
