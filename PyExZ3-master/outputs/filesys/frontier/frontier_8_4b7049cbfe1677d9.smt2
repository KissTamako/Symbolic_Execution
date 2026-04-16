(set-logic ALL)
; Frontier Constraint ID: 4b7049cbfe1677d9
; Generated at: 2026-04-16 15:10:06
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1024)) (False)
(assert (not (not (= x 1024))))

(check-sat)
(get-model)
