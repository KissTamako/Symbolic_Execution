(set-logic ALL)
; Frontier Constraint ID: 685c00d991e597f9
; Generated at: 2026-04-17 03:12:47
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2827)) (False)
(assert (not (not (= x 2827))))

(check-sat)
(get-model)
