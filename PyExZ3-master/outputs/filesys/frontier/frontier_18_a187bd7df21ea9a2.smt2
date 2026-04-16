(set-logic ALL)
; Frontier Constraint ID: a187bd7df21ea9a2
; Generated at: 2026-04-16 14:57:49
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 889)) (False)
(assert (not (not (= x 889))))

(check-sat)
(get-model)
