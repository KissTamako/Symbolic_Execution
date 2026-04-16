(set-logic ALL)
; Constraint ID: b1b5fbb774651dbf
; Generated at: 2026-04-16 11:54:14
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60619)) (False)
(assert (not (not (= x 60619))))

(check-sat)
(get-model)
