(set-logic ALL)
; Frontier Constraint ID: c7d1c75ebc9a851f
; Generated at: 2026-04-16 14:57:49
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 895)) (False)
(assert (not (not (= x 895))))

(check-sat)
(get-model)
