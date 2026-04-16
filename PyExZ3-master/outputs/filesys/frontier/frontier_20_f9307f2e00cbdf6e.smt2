(set-logic ALL)
; Frontier Constraint ID: f9307f2e00cbdf6e
; Generated at: 2026-04-16 14:44:34
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 742)) (False)
(assert (not (not (= x 742))))

(check-sat)
(get-model)
