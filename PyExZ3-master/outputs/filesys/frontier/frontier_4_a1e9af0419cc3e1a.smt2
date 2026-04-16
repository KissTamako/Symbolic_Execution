(set-logic ALL)
; Constraint ID: a1e9af0419cc3e1a
; Generated at: 2026-04-16 11:54:14
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60592)) (False)
(assert (not (not (= x 60592))))

(check-sat)
(get-model)
