(set-logic ALL)
; Constraint ID: 2797aaf0dc296624
; Generated at: 2026-04-16 11:49:33
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60457)) (False)
(assert (not (not (= x 60457))))

(check-sat)
(get-model)
