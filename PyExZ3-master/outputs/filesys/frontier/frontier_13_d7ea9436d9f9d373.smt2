(set-logic ALL)
; Frontier Constraint ID: d7ea9436d9f9d373
; Generated at: 2026-04-16 14:41:51
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 505)) (False)
(assert (not (= x 505)))

; Query: ((== x 506)) (False)
(assert (not (not (= x 506))))

(check-sat)
(get-model)
