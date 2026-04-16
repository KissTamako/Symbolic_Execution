(set-logic ALL)
; Frontier Constraint ID: faa0620fd1a7de0a
; Generated at: 2026-04-16 16:02:53
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1717)) (False)
(assert (not (not (= x 1717))))

(check-sat)
(get-model)
