(set-logic ALL)
; Frontier Constraint ID: f968a2c81936c36a
; Generated at: 2026-04-17 01:52:09
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1849)) (False)
(assert (not (not (= x 1849))))

(check-sat)
(get-model)
