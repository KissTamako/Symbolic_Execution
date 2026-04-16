(set-logic ALL)
; Frontier Constraint ID: 269367438e489621
; Generated at: 2026-04-17 01:52:09
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1837)) (False)
(assert (not (not (= x 1837))))

(check-sat)
(get-model)
