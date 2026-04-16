(set-logic ALL)
; Constraint ID: 6a6b32b00d544f07
; Generated at: 2026-04-16 11:49:33
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60451)) (False)
(assert (not (not (= x 60451))))

(check-sat)
(get-model)
