(set-logic ALL)
; Frontier Constraint ID: 4949e70ebcb5277f
; Generated at: 2026-04-16 15:56:50
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1645)) (False)
(assert (not (not (= x 1645))))

(check-sat)
(get-model)
