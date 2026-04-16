(set-logic ALL)
; Constraint ID: 4c3d640c9abeb8ce
; Generated at: 2026-04-16 04:51:40
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59398)) (False)
(assert (not (not (= x 59398))))

(check-sat)
(get-model)
