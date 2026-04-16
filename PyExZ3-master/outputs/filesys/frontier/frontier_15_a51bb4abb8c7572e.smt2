(set-logic ALL)
; Frontier Constraint ID: a51bb4abb8c7572e
; Generated at: 2026-04-16 14:36:25
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 358)) (False)
(assert (not (= x 358)))

; Query: ((== x 359)) (False)
(assert (not (not (= x 359))))

(check-sat)
(get-model)
