(set-logic ALL)
; Constraint ID: 26c61abf92fea5ca
; Generated at: 2026-04-16 11:31:08
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60070)) (False)
(assert (not (not (= x 60070))))

(check-sat)
(get-model)
