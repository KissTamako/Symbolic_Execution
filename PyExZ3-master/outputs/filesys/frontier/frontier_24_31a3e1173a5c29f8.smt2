(set-logic ALL)
; Frontier Constraint ID: 31a3e1173a5c29f8
; Generated at: 2026-04-16 15:56:50
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1648)) (False)
(assert (not (not (= x 1648))))

(check-sat)
(get-model)
