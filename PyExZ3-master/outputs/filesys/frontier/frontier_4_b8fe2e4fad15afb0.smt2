(set-logic ALL)
; Frontier Constraint ID: b8fe2e4fad15afb0
; Generated at: 2026-04-16 15:26:57
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1318)) (False)
(assert (not (not (= x 1318))))

(check-sat)
(get-model)
