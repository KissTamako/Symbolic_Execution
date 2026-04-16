(set-logic ALL)
; Frontier Constraint ID: a5f0bcd72765f75c
; Generated at: 2026-04-16 14:36:25
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 349)) (False)
(assert (not (= x 349)))

; Query: ((== x 350)) (False)
(assert (not (not (= x 350))))

(check-sat)
(get-model)
