(set-logic ALL)
; Frontier Constraint ID: c79ebf5bddc87c09
; Generated at: 2026-04-16 14:41:51
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 493)) (False)
(assert (not (= x 493)))

; Query: ((== x 494)) (False)
(assert (not (not (= x 494))))

(check-sat)
(get-model)
