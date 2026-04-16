(set-logic ALL)
; Frontier Constraint ID: fe393ccb5998d31b
; Generated at: 2026-04-16 15:10:06
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1033)) (False)
(assert (not (not (= x 1033))))

(check-sat)
(get-model)
