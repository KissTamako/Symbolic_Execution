(set-logic ALL)
; Frontier Constraint ID: 967aa4da6db3422f
; Generated at: 2026-04-17 02:51:35
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2446)) (False)
(assert (not (not (= x 2446))))

(check-sat)
(get-model)
