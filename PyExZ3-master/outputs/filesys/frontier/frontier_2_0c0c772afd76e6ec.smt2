(set-logic ALL)
; Constraint ID: 0c0c772afd76e6ec
; Generated at: 2026-04-16 11:31:08
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60064)) (False)
(assert (not (not (= x 60064))))

(check-sat)
(get-model)
