(set-logic ALL)
; Constraint ID: 16dfd1e802b8c5a1
; Generated at: 2026-04-16 11:43:57
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60286)) (False)
(assert (not (= x 60286)))

; Query: ((== x 60287)) (False)
(assert (not (not (= x 60287))))

(check-sat)
(get-model)
