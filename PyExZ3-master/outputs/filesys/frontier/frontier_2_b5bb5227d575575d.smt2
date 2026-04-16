(set-logic ALL)
; Frontier Constraint ID: b5bb5227d575575d
; Generated at: 2026-04-16 14:43:36
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 640)) (False)
(assert (not (not (= x 640))))

(check-sat)
(get-model)
