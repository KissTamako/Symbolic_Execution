(set-logic ALL)
; Frontier Constraint ID: 0742250f63d54049
; Generated at: 2026-04-16 16:02:53
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1708)) (False)
(assert (not (not (= x 1708))))

(check-sat)
(get-model)
