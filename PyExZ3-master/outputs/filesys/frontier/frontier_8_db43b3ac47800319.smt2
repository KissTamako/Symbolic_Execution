(set-logic ALL)
; Constraint ID: db43b3ac47800319
; Generated at: 2026-04-16 11:40:22
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60148)) (False)
(assert (not (not (= x 60148))))

(check-sat)
(get-model)
