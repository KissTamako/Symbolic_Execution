(set-logic ALL)
; Constraint ID: ca411b16e848c565
; Generated at: 2026-04-16 04:08:23
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59266)) (False)
(assert (not (not (= x 59266))))

(check-sat)
(get-model)
