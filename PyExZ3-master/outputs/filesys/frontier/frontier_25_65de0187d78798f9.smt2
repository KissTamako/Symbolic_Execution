(set-logic ALL)
; Frontier Constraint ID: 65de0187d78798f9
; Generated at: 2026-04-17 01:52:09
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1873)) (False)
(assert (not (= x 1873)))

; Query: ((== x 1874)) (False)
(assert (not (not (= x 1874))))

(check-sat)
(get-model)
