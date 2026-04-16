(set-logic ALL)
; Frontier Constraint ID: fb686af714d087db
; Generated at: 2026-04-17 02:51:35
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2449)) (False)
(assert (not (not (= x 2449))))

(check-sat)
(get-model)
