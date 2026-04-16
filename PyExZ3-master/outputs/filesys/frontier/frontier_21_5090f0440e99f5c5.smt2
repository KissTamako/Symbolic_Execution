(set-logic ALL)
; Frontier Constraint ID: 5090f0440e99f5c5
; Generated at: 2026-04-16 14:36:25
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 367)) (False)
(assert (not (= x 367)))

; Query: ((== x 368)) (False)
(assert (not (not (= x 368))))

(check-sat)
(get-model)
