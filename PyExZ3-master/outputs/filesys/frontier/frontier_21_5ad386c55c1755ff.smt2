(set-logic ALL)
; Constraint ID: 5ad386c55c1755ff
; Generated at: 2026-04-16 11:54:14
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60616)) (False)
(assert (not (= x 60616)))

; Query: ((== x 60617)) (False)
(assert (not (not (= x 60617))))

(check-sat)
(get-model)
