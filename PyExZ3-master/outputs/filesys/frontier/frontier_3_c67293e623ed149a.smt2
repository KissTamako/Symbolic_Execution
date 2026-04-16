(set-logic ALL)
; Frontier Constraint ID: c67293e623ed149a
; Generated at: 2026-04-17 02:51:35
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2440)) (False)
(assert (not (= x 2440)))

; Query: ((== x 2441)) (False)
(assert (not (not (= x 2441))))

(check-sat)
(get-model)
