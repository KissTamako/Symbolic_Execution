(set-logic ALL)
; Frontier Constraint ID: 09dc24b88cfb8d39
; Generated at: 2026-04-16 15:10:06
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1021)) (False)
(assert (not (= x 1021)))

; Query: ((== x 1022)) (False)
(assert (not (not (= x 1022))))

(check-sat)
(get-model)
