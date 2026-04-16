(set-logic ALL)
; Frontier Constraint ID: 44b209aa5d313cef
; Generated at: 2026-04-16 13:27:43
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((> x 0)) (False)
(assert (not (not (> x 0))))

(check-sat)
(get-model)
