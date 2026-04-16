(set-logic ALL)
; Frontier Constraint ID: ab48f22662ae23ac
; Generated at: 2026-04-16 14:42:45
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 592)) (False)
(assert (not (not (= x 592))))

(check-sat)
(get-model)
