(set-logic ALL)
; Frontier Constraint ID: 6b5759ba3f169869
; Generated at: 2026-04-16 15:10:06
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1039)) (False)
(assert (not (not (= x 1039))))

(check-sat)
(get-model)
