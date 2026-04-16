(set-logic ALL)
; Frontier Constraint ID: 07a8e4aa9b5616a1
; Generated at: 2026-04-16 14:41:51
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 487)) (False)
(assert (not (= x 487)))

; Query: ((== x 488)) (False)
(assert (not (not (= x 488))))

(check-sat)
(get-model)
