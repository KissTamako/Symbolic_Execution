(set-logic ALL)
; Frontier Constraint ID: 5551167486d1e1b7
; Generated at: 2026-04-16 15:16:56
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1174)) (False)
(assert (not (not (= x 1174))))

(check-sat)
(get-model)
