(set-logic ALL)
; Frontier Constraint ID: 99d5c1bd4075b243
; Generated at: 2026-04-16 14:57:49
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 862)) (False)
(assert (not (= x 862)))

; Query: ((== x 863)) (False)
(assert (not (not (= x 863))))

(check-sat)
(get-model)
